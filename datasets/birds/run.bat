mkdir backgroundless_images;
mkdir background;
mkdir edges;
mkdir backgroundless_edges;

python D:\Documents\image-to-outline\bin\main.py images backgroundless_images 1
python D:\Documents\image-to-outline\run.py bsds500 images edges
python D:\Documents\image-to-outline\outline.py edges backgroundless_images backgroundless_edges

python split.py "256x256 images" backgroundless_images "256x256 edges" backgroundless_edges

python D:\Documents\image-to-outline\run.py bsds500 images edges 9 75 75
