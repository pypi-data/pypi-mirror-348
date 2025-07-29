This is the official Pytorch implementation of 2pCePd-Net model published in IEEE Transactions on Instrumentation and Measurement

DOI: 10.1109/TIM.2025.3569005

Model Sample Usage Code:

# from two_pcepd import model

# network, optimizer = model.create_net(in_ch, out_ch, dim, n)

in_ch -> the number of channels in input

out_ch -> the number of channels in output

dim -> a dimensional parameter to modulate the number of parameters in the model. Default value is 64. Reducing or increasing the parameters would modulate the model accordingly.

n -> number of paths. Default value is 2. Can be modulated to increase or decrease the complexity of the model.

network -> the returned model

optimizer -> the optimizer associated with network is returned. Default value is Adam Optimizer with learning rate set to 1e^-4