import torch
from copy import deepcopy

from facexlib.utils import load_file_from_url
from .retinaface import RetinaFace


def init_detection_model(model_name, half=False, device='cuda'):
    if model_name == 'retinaface_resnet50':
        model = RetinaFace(network_name='resnet50', half=half)
        model_url = 'experiments/pretrained_models/detection_Resnet50_Final.pth'
    elif model_name == 'retinaface_mobile0.25':
        model = RetinaFace(network_name='mobile0.25', half=half)
        model_url = 'https://github.com/xinntao/facexlib/releases/download/v0.1.0/detection_mobilenet0.25_Final.pth'
    else:
        raise NotImplementedError(f'{model_name} is not implemented.')

    if model_url.startswith('https://'):
        model_path = load_file_from_url(url=model_url, model_dir='facexlib/weights', progress=True, file_name=None)
    else:
        model_path = model_url
    # TODO: clean pretrained model
    load_net = torch.load(model_path, map_location=lambda storage, loc: storage)
    # remove unnecessary 'module.'
    for k, v in deepcopy(load_net).items():
        if k.startswith('module.'):
            load_net[k[7:]] = v
            load_net.pop(k)
    model.load_state_dict(load_net, strict=True)
    model.eval()
    model = model.to(device)
    return model
