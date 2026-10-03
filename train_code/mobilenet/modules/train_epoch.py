from tqdm import tqdm
import modules.metrics as metrics
import torch

def get_lr(optimizer):
    for param_group in optimizer.param_groups:
        return param_group['lr']

def train_fn(loader, model, optimizer, loss_fn, device):
    
    print(f'Learning Rate = {get_lr(optimizer=optimizer)}\n')

    model.train()
    loop = tqdm(loader, desc='Training', leave=True)
    train_losses = []
    smoke_losses = []
    fire_losses = []

    for batch_idx, (x, y) in enumerate(loop):
        x, y = x.to(device), y.to(device)
        out = model(x)
        train_loss = loss_fn(ground_truth=y, 
                             predictions=out)

        # Gradient Descent
        optimizer.zero_grad()
        train_loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=10.0)
        optimizer.step()
        # if hasattr(model, 'clip_weights'):
        #     model.clip_weights(-1, 1)

        # BCE Loss
        last_losses = loss_fn.get_last_losses()
        train_losses.append(train_loss.item())
        smoke_losses.append(last_losses['smoke_loss'])
        fire_losses.append(last_losses['fire_loss'])
        
        yhat = torch.sigmoid(out.detach()) # Not needed, metrics understand that input is Logits
        metrics.precision_metric.update(yhat, y)
        metrics.recall_metric.update(yhat, y)
        metrics.accuracy_metric.update(yhat, y)
        metrics.f1_metric.update(yhat, y)
          
    train_mean_loss = sum(train_losses)/len(train_losses)
    smoke_mean_loss = sum(smoke_losses)/len(smoke_losses)
    fire_mean_loss = sum(fire_losses)/len(fire_losses)

    print("Total Loss".ljust(12) + "|" + 
          "Smoke Loss".ljust(12) + "|" + 
          "Fire Loss".ljust(12))
    print("------------".ljust(12) + " " + 
          "------------".ljust(12) + " " + 
          "------------".ljust(12))
    print(f'{train_mean_loss:.3f}'.ljust(12) + "|" +
          f'{smoke_mean_loss:.3f}'.ljust(12) + "|" +
          f'{fire_mean_loss:.3f}'.ljust(12) + "\n")
    
    precision = metrics.precision_metric.compute()
    recall = metrics.recall_metric.compute()
    accuracy = metrics.accuracy_metric.compute()
    f1 = metrics.f1_metric.compute()
    
    metrics.precision_metric.reset()
    metrics.recall_metric.reset()
    metrics.accuracy_metric.reset()
    metrics.f1_metric.reset()
   
    return (
        {
        'Total': train_mean_loss, 
        'Smoke': smoke_mean_loss, 
        'Fire': fire_mean_loss
        },
        {
        'Accuracy': [accuracy[0].item(), accuracy[1].item()],
        'Precision': [precision[0].item(), precision[1].item()],
        'Recall': [recall[0].item(), recall[1].item()],
        'F1': [f1[0].item(), f1[1].item()] 
        }
    )

def fog_train_fn(loader, model, optimizer, loss_fn, device):
    
    print(f'Learning Rate = {get_lr(optimizer=optimizer)}\n')

    model.train()
    loop = tqdm(loader, desc='Training', leave=True)
    train_losses = []

    for batch_idx, (x, y) in enumerate(loop):
        x, y = x.to(device), y.to(device)
        yhat = model(x)
        train_loss = loss_fn(ground_truth=y, 
                             predictions=yhat)
      
        # Gradient Descent
        optimizer.zero_grad()
        train_loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=10.0)
        optimizer.step()

        # CE Loss
        train_losses.append(train_loss.item())
        
        yhat = torch.argmax(yhat, dim=1).detach()
        y = torch.argmax(y, dim=1).detach()
        # print(f'Batch {batch_idx}: YHAT \n{yhat}')
        # print(f'Batch {batch_idx}: TARGET \n{y}')
        metrics.fog_precision_metric.update(yhat, y)
        metrics.fog_recall_metric.update(yhat, y)
        metrics.fog_accuracy_metric.update(yhat, y)
        metrics.fog_f1_metric.update(yhat, y)
          
    train_mean_loss = sum(train_losses)/len(train_losses)
    
    precision = metrics.fog_precision_metric.compute()
    recall = metrics.fog_recall_metric.compute()
    accuracy = metrics.fog_accuracy_metric.compute()
    f1 = metrics.fog_f1_metric.compute()
    
    metrics.fog_precision_metric.reset()
    metrics.fog_recall_metric.reset()
    metrics.fog_accuracy_metric.reset()
    metrics.fog_f1_metric.reset()
    
    print(f'Total Train Loss: {train_mean_loss:.3f}')
    # print(f'Precision: {precision:.4f} - Recall: {recall:.4f} - Accuracy: {accuracy:.4f} - F1: {f1:.4f}')
    print(f'Precision: {precision} \nRecall: {recall} \nAccuracy: {accuracy} \nF1: {f1}')
    
    return (
        {
        'Total': train_mean_loss, 
        },
        {
        'Accuracy': accuracy,
        'Precision': precision,
        'Recall': recall,
        'F1': f1
        }
    )


def fog_binary_train_fn(loader, model, optimizer, loss_fn, device):
    
    print(f'Learning Rate = {get_lr(optimizer=optimizer)}\n')

    model.train()
    loop = tqdm(loader, desc='Training', leave=True)
    train_losses = []

    for batch_idx, (x, y) in enumerate(loop):
        x, y = x.to(device), y.to(device)
        yhat = model(x)
        train_loss = loss_fn(ground_truth=y, 
                             predictions=yhat)
      
        # Gradient Descent
        optimizer.zero_grad()
        train_loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=10.0)
        optimizer.step()

        # CE Loss
        train_losses.append(train_loss.item())
        
        yhat = torch.sigmoid(yhat.detach())
        # print(f'Batch {batch_idx}: YHAT \n{yhat}')
        # print(f'Batch {batch_idx}: TARGET \n{y}')
        metrics.fog_binary_precision_metric.update(yhat, y)
        metrics.fog_binary_recall_metric.update(yhat, y)
        metrics.fog_binary_accuracy_metric.update(yhat, y)
        metrics.fog_binary_f1_metric.update(yhat, y)
          
    train_mean_loss = sum(train_losses)/len(train_losses)
    
    precision = metrics.fog_binary_precision_metric.compute()
    recall = metrics.fog_binary_recall_metric.compute()
    accuracy = metrics.fog_binary_accuracy_metric.compute()
    f1 = metrics.fog_binary_f1_metric.compute()
    
    metrics.fog_binary_precision_metric.reset()
    metrics.fog_binary_recall_metric.reset()
    metrics.fog_binary_accuracy_metric.reset()
    metrics.fog_binary_f1_metric.reset()
    
    print(f'Total Train Loss: {train_mean_loss:.3f}')
    print(f'Precision: {precision:.4f} - Recall: {recall:.4f} - Accuracy: {accuracy:.4f} - F1: {f1:.4f}')
    
    return (
        {
        'Total': train_mean_loss, 
        },
        {
        'Accuracy': accuracy,
        'Precision': precision,
        'Recall': recall,
        'F1': f1
        }
    )