from hs_rnn import Neural_Network 
from hearthstoneAPI import HearthstoneAPI



nn = Neural_Network()

api = HearthstoneAPI()

api.getLastestSet()
api.getCardsByParam('sets', 'Basic')

#nn.startTraining()
#nn.StartGenerating(1000)