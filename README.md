# JetbotHandDetect
Transfer Learning 을 이용한 손모양 supervise, detect 를 jetbot에 마운트하여 
손동작에 따라서 움직이는 프로젝트
* * *

### labeling
```
meta_train = []
meta_valid = []
for root, dirs, filenames in os.walk('hand_detection'):
    if 'train' in root:
        meta = meta_train
    elif 'valid' in root:
        meta = meta_valid
    else:
        continue


    for filename in filenames:
        first, last = os.path.splitext(filename)
        if last != '.jpg':
            continue
        label = -1
        for name in labels:
            if name in filename:
                label = labels[name]
                break
        if label == -1:
            continue
        
        path = os.path.join(root, filename)
        meta.append((path, label))

len(meta_train), len(meta_valid)
```
