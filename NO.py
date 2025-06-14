import argparse
import pickle
import torch
import torch.optim as optim


from utils.NO_data import extract_data, create_data_driven_data_loader
from utils.NO_training import train, plot, test
from models.FNO import  data_driven_FNO_Model
from models.Unet import data_driven_Unet_Model
from models.U_FNO import data_driven_UFNO_Model
from models.WNO import data_driven_WNO_Model

# set arguments
parser = argparse.ArgumentParser(description='command setting')
parser.add_argument('--phase', type=str, default='test')
parser.add_argument('--model', type=str, default='WNO')
parser.add_argument('--data', type=str, default='homo')
parser.add_argument('--train_method', type=str, default='NO')
parser.add_argument('--epochs', type=int, default=500)
args = parser.parse_args()

# load the data
if args.data == 'heter':
    with open('./simulation/data_general_heter.pkl', 'rb') as handle:
        mat_contents = pickle.load(handle)
    data = extract_data(mat_contents)
elif args.data == 'homo':
    with open('./simulation/data_general_incom.pkl', 'rb') as handle:
        mat_contents = pickle.load(handle)
    data = extract_data(mat_contents)
train_loader, val_loader, test_loader = create_data_driven_data_loader(data, [0.7,0.8], 1, train_shuffle=False)
print(len(train_loader), len(val_loader), len(test_loader))

# define devices
device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

# define model
if args.model == 'FNO':
    model =  data_driven_FNO_Model().float().to(device)
elif args.model == 'Unet':
    model = data_driven_Unet_Model().float().to(device)
elif args.model == 'UFNO':
    model = data_driven_UFNO_Model().float().to(device)
elif args.model == 'WNO':
    model = data_driven_WNO_Model().float().to(device)

# try loading pre-trained model
try:
    model.load_state_dict(torch.load(r'./trained_models/{}_{}_{}.pth'.format(args.model, args.data, args.train_method)))
except:
    print('No pre-trained model.')

# define optimizer
optimizer = optim.Adam(model.parameters(), lr=0.001)

if args.phase == 'plot_train':
    if args.data == 'heter':
        args.data = 'heter_train'
    if args.data == 'homo':
        args.data = 'homo_train'
    test_loader = train_loader

# exp
if args.phase == 'train':
    model = model.to(device)
    train(args, model, device, (train_loader, val_loader, test_loader), optimizer)
elif args.phase == 'test':
    model = model.to(device)
    err = test(args, model, device, test_loader)
    print('average relative error:', err)
elif args.phase == 'plot' or args.phase == 'plot_train':
    model = model.to(device)
    plot(args, model, device, test_loader)
