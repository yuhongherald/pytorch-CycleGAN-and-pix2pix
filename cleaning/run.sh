
#python extract.py
#python resize.py

cd ..

python datasets/combine_A_and_B.py --fold_A datasets/Macaws/contoured_cut --fold_B datasets/Macaws/contoured_outlines --fold_AB datasets/Macaws/contoured-cut-outlines

python train.py --dataroot ./datasets/birds --name edge2birds --model pix2pix --direction BtoA --preprocess resize --load_size 64 --crop_size 64 --no_flip --netG unet_64 --netD n_layers --n_layers_D 2 --save_latest_freq 1163 --save_epoch_freq 20 --display_id 0 --niter 200 --niter_decay 0 --batch_size 4

# Epoch 179 - Rmb to add
python train.py --dataroot ./datasets/birds --name edge2birds --model pix2pix --direction BtoA --preprocess resize --load_size 64 --crop_size 64 --no_flip --netG unet_64 --netD n_layers --n_layers_D 2 --save_latest_freq 1334 --save_epoch_freq 20 --display_id 0 --niter 200 --niter_decay 0 --batch_size 4 --continue_train --epoch_count 179

# Epoch 79
python train.py --dataroot ./datasets/birds --name edge2birds --model pix2pix --direction BtoA --preprocess resize --load_size 64 --crop_size 64 --no_flip --netG unet_64 --netD n_layers --n_layers_D 2 --save_latest_freq 1654 --save_epoch_freq 20 --display_id 0 --niter 200 --niter_decay 0 --batch_size 16 --continue_train --epoch_count 79
python test.py --dataroot ./datasets/birds --name edge2birds --model pix2pix --direction BtoA --preprocess resize --load_size 64 --crop_size 64 --no_flip --netG unet_64 --netD n_layers --n_layers_D 2
