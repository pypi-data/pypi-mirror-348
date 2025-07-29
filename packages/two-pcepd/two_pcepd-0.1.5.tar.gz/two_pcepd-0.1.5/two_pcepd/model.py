import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim

class ProbAttention(nn.Module):
    def __init__(self, ch, n_heads = 2):
        super().__init__()
        
        self.n_heads = n_heads
        
        self.q_mappings = nn.ModuleList([nn.Conv2d(ch, ch, kernel_size=3, stride=1, padding=1, bias=False, groups=ch) for _ in range(self.n_heads)])
        self.k_mappings = nn.ModuleList([nn.Conv2d(ch, ch, kernel_size=3, stride=1, padding=1, bias=False, groups=ch) for _ in range(self.n_heads)])
        self.v_mappings = nn.ModuleList([nn.Conv2d(ch, ch, kernel_size=3, stride=1, padding=1, bias=False, groups=ch) for _ in range(self.n_heads)])
        
        self.out_map = nn.Conv2d(n_heads * ch, ch, kernel_size=3, stride=1, padding=1, bias=True)
        
        for head in range(self.n_heads):
            nn.init.xavier_normal_(self.k_mappings[head].weight)
            nn.init.xavier_normal_(self.v_mappings[head].weight)
        
        nn.init.xavier_normal_(self.out_map.weight)
        
        nn.init.zeros_(self.out_map.bias)
        
        self.softmax = nn.Softmax(dim=-1)
        
        self.cv = nn.Conv2d(ch,ch,kernel_size=1, stride=1, bias=False)
                
    def forward(self, x, h_1):
        # x is the input tensor for this layer
        # h_1 is the probability map value from previous iteration of this layer
        
        result = []
        for head in range(self.n_heads):
            q_mapping = self.q_mappings[head]
            k_mapping = self.k_mappings[head]
            v_mapping = self.v_mappings[head]
            
            q, k, v = q_mapping(h_1), k_mapping(x), v_mapping(x)
            
            A = self.softmax(torch.mul(q, k) / ((x.shape[1]*x.shape[2]) ** 0.5))
            
            fg = torch.mul(A, v)
            
            h = x+fg
            
            result.append(h)
                    
        return self.out_map(torch.cat([r for r in result], dim=1))
    
class UpAttention(nn.Module):
    """Upscaling then double conv"""

    def __init__(self, ch):
        super().__init__()

        self.up = nn.ConvTranspose2d(ch, ch//2, kernel_size=2, stride=2)
        
    def forward(self, x):
        return self.up(x)
    
class EncoderAttention(nn.Module):
    def __init__(self, ch):
        super().__init__()
        
        self.forget_gate = nn.Conv2d(ch, ch, kernel_size=1, stride=1, bias=False)
        self.forget_sig = nn.Sigmoid()
        
        self.in_gate_1 = nn.Conv2d(ch, ch, kernel_size=1, stride=1, bias=False)
        self.in_gate_2 = nn.Conv2d(ch, ch, kernel_size=1, stride=1, bias=False)
        self.in_sig = nn.Sigmoid()
        self.in_tanh = nn.Tanh()
        
        self.out_gate_1 = nn.Conv2d(ch, ch, kernel_size=1, stride=1, bias=False)
        self.out_gate_2 = nn.Conv2d(ch, ch, kernel_size=1, stride=1, bias=False)
        self.out_sig = nn.Sigmoid()
        self.out_tanh = nn.Tanh()
        
    def forward(self, x, x_):
        C_fg = x*self.forget_sig(self.forget_gate(x_))
        C_fg = C_fg + self.in_sig(self.in_gate_1(x_))*self.in_tanh(self.in_gate_2(x_))
        out = self.out_tanh(self.out_gate_1(C_fg)) * self.out_sig(self.out_gate_2(x_))
        
        return out
    
class DoubleConv(nn.Module):
    """(convolution => [BN] => ReLU) * 2"""

    def __init__(self, in_channels, out_channels, kernel,pad):
        super().__init__()
        
        if(in_channels==1):
            mid_channels = in_channels
        else:
            mid_channels = in_channels//2
        
        self.double_conv = nn.Sequential(
            nn.Conv2d(in_channels, mid_channels, kernel_size=1, padding=0, bias=False),
            nn.BatchNorm2d(mid_channels),
            nn.LeakyReLU(0.2),
            nn.Conv2d(mid_channels, out_channels, kernel_size=kernel, padding=pad, bias=False),
            nn.BatchNorm2d(out_channels),
            nn.LeakyReLU(0.2)
        )

    def forward(self, x):
        return self.double_conv(x)
    
class DoubleConv2(nn.Module):
    """(convolution => [BN] => ReLU) * 2"""

    def __init__(self, in_channels, out_channels, kernel,pad):
        super().__init__()
        
        mid_channels = in_channels
        
        self.double_conv = nn.Sequential(
            nn.Conv2d(in_channels, mid_channels, kernel_size=3, padding=1, bias=False),
            nn.BatchNorm2d(mid_channels),
            nn.LeakyReLU(0.2),
            nn.Conv2d(mid_channels, out_channels, kernel_size=kernel, padding=pad, bias=False),
            nn.BatchNorm2d(out_channels),
            nn.LeakyReLU(0.2)
        )

    def forward(self, x):
        return self.double_conv(x)
    
class Down(nn.Module):
    """Downscaling with maxpool then double conv"""

    def __init__(self, in_channels, out_channels, kernel=3, pad=1, n=2):
        super().__init__()
        self.pool = nn.MaxPool2d(2)
        self.prob = ProbAttention(in_channels, n_heads = n)
        self.conv = DoubleConv(in_channels, out_channels, kernel, pad)
        
    def forward(self, x, x_):
        pool = self.pool(x)
        prob = self.prob(pool, x_)
        out = self.conv(prob)
        
        return out
    
class Down2(nn.Module):
    """Downscaling with maxpool then double conv"""

    def __init__(self, in_channels, out_channels, kernel=3, pad=1):
        super().__init__()
        self.pool = nn.MaxPool2d(2)
        self.conv = DoubleConv(in_channels, out_channels, kernel, pad)
        
    def forward(self, x, x_):
        pool = self.pool(x)
        out = self.conv(pool)
        
        return out
    
class Bottleneck(nn.Module):
    
    def __init__(self, ch):
        super().__init__()
        
        self.up = UpAttention(2*ch)
        self.lstm = EncoderAttention(ch)
        
    def forward(self, x, x_):
        mod = self.up(x_)
        out = self.lstm(x,mod)
        
        return torch.cat([out,mod], dim=1)
    
class Up(nn.Module):
    """Upscaling then double conv"""

    def __init__(self, in_channels, out_channels, kernel=3, pad=1):
        super().__init__()

        self.up = nn.ConvTranspose2d(in_channels, in_channels // 2, kernel_size=2, stride=2)
        self.conv = DoubleConv((3*in_channels)//2, out_channels, kernel=3, pad=1)
        
    def forward(self, x1, x2):
        x1 = self.up(x1)
        diffY = x2.size()[2] - x1.size()[2]
        diffX = x2.size()[3] - x1.size()[3]

        x1 = F.pad(x1, [diffX // 2, diffX - diffX // 2,
                        diffY // 2, diffY - diffY // 2])

        x = torch.cat([x2, x1], dim=1)
        return self.conv(x)

class OutConv(nn.Module):
    def __init__(self, in_channels, out_channels):
        super(OutConv, self).__init__()
        self.conv = nn.Conv2d(in_channels, out_channels, kernel_size=1)
        self.sigma = nn.Sigmoid()

    def forward(self, x):
        return self.sigma(self.conv(x))
    
class Fusion(nn.Module):
    def __init__(self, batch, d):
        super().__init__()
        
        self.cv1 = nn.Conv2d(d, d, kernel_size=1, bias=False)
        self.pb1 = nn.Conv2d(d, 1, kernel_size=1, bias=False)
        
        self.cv2 = nn.Conv2d(d, d//2, kernel_size=1, bias=False)
        self.pb2 = nn.Conv2d(1, d//2, kernel_size=1, bias=False)
        
        self.cv3 = nn.Conv2d(d//2, d, kernel_size=1, bias=False)
        self.pb3 = nn.Conv2d(d//2, d, kernel_size=1, bias=False)
        
        self.merge1 = nn.Conv2d(d, d, kernel_size=1, bias=False)
        self.merge2 = nn.Conv2d(d*2, d, kernel_size=1, bias=False)
        
        self.conv1 = nn.Conv2d(d*2, d, kernel_size=1, bias=False)
        self.conv2 = nn.Conv2d(d, d//2, kernel_size=1, bias=False)
        self.conv3 = nn.Conv2d(d//2, 1, kernel_size=1, bias=False)
        
        self.sigma1 = nn.Sigmoid()
        self.sigma2 = nn.Sigmoid()
        
        self.sig = nn.Sigmoid()
        
    def forward(self, x1, x2):
        x = self.cv1(x1) #64 -> 64
        p = self.pb1(x2) #64 -> 1
        
        x = self.cv2(x) #64 -> 32
        p = self.pb2(p) #1 -> 32
        
        m1 = self.merge1(torch.cat([x,p], dim=1)) # 32+32 = 64
        
        x = self.cv3(x) #32 -> 64 
        p = self.pb3(p) #32 -> 64
        
        m2 = self.merge2(torch.cat([x,p], dim=1)) #64+64 = 128 -> 64
        
        m2 = m2 - self.sigma1(m2)
        m1 = m1 + self.sigma2(m1)
        
        m = torch.cat([m1, m2], dim=1)
        
        m = self.conv1(m) # 128->64
        m = self.conv2(m) # 64->32
        m = self.conv3(m) # 32->1
        
        return self.sig(m), m1, m2#, low, up        
    
class UNet(nn.Module):
    def __init__(self, n_channels, n_classes, d=2, n_heads=2):
        super(UNet, self).__init__()
        self.n_channels = n_channels
        self.n_classes = n_classes
        self.d = d

        self.inc = (DoubleConv(n_channels, d, kernel=3, pad=1))
        
        # Encoder part for primary network
        self.down1 = (Down(d, d*2, kernel=3, pad=1, n=n_heads))
        self.down2 = (Down(d*2, d*4, kernel=3, pad=1, n=n_heads))
        self.down3 = (Down(d*4, d*8, kernel=3, pad=1, n=n_heads))
        self.down4 = (Down(d*8, d*16, kernel=3, pad=1, n=n_heads))
        
        # Encoder part for secondary network
        self.down_1 = nn.Conv2d(n_channels, d, kernel_size=3, stride=2, padding=1, bias=False)
        self.down_2 = nn.Conv2d(d, d*2, kernel_size=3, stride=2, padding=1, bias=False)
        self.down_3 = nn.Conv2d(d*2, d*4, kernel_size=3, stride=2, padding=1, bias=False)
        self.down_4 = nn.Conv2d(d*4, d*8, kernel_size=3, stride=2, padding=1, bias=False)
        
        # Bottleneck part of each layer
        
        self.bottle3 = Bottleneck(d*8)
        self.bottle2 = Bottleneck(d*4)
        self.bottle1 = Bottleneck(d*2)
        self.bottle = Bottleneck(d)
        
        # Decoder part of network
        
        self.up1 = (Up(d*16, d*8, kernel=3, pad=1))
        
        self.up2 = (Up(d*8, d*4, kernel=3, pad=1))
        self.up3 = (Up(d*4, d*2, kernel=3, pad=1))
        self.up4 = (Up(d*2, d, kernel=3, pad=1))
        self.outc = (OutConv(d, n_classes))
        

    def forward(self, x):
        # Encoder layer 1
        x1 = self.inc(x)
        d1 = self.down_1(x)
        x2 = self.down1(x1, d1)
        
        # Encoder layer 2
        d2 = self.down_2(d1)
        x3 = self.down2(x2, d2)
        
        # Encoder layer 3
        d3 = self.down_3(d2)
        x4 = self.down3(x3, d3)
        
        # Encoder layer 4
        d4 = self.down_4(d3)
        x5 = self.down4(x4, d4)
        
        # Decoder layer 1
        x = self.up1(x5,self.bottle3(x4,x5))
        
        # Decoder layer 2
        x = self.up2(x,self.bottle2(x3,x4))
        
        # Decoder layer 3
        x = self.up3(x,self.bottle1(x2,x3))

        # Decoder layer 4
        x = self.up4(x,self.bottle(x1,x2))
        
        pred = self.outc(x)
        
        return pred
    
def create_net(in_ch=1, out_ch=1, dim=64, n=2):
    torch.manual_seed(0)
    torch.use_deterministic_algorithms(False)

    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    
    unet = UNet(in_ch,out_ch,d=dim, n_heads=n)
    unet.to(device, dtype=torch.float)
    opt = optim.Adam(unet.parameters(), lr = 1e-4)
    
    return unet,opt