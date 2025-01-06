# TODO

Check these tools.  
- How easy it is to do batch exports ?  
- Create batch export tools for most promising solutions.  
- Move tested tools to the done section and add a small comment

(Not an exhaustive list, feel free to complete it)

## GUI tools
### Windows only
-	xNormal
-	ShaderMap
-	Materialize
### All platforms
-	Laigter : https://azagaya.itch.io/laigter
- 	Photoshop 3d filter
-	Blender 
-	Sprite Lamp
## IA
-	Stable Diffusion
-	ControlNet : https://huggingface.co/lllyasviel/sd-controlnet-normal


<br><br>

# Done
## Material Map Generator

https://github.com/joeyballentine/Material-Map-Generator  
On mac :

    py generate.py --cpu

## Online tools 

- NormalMap-Online : https://cpetry.github.io/NormalMap-Online/  
        Grayscal technique -> lame
- SmartNormal : https://www.smart-page.net/smartnormal/  
		Grayscal technique -> better but still meh

## Imaginairy normal map

https://github.com/brycedrennan/imaginairy-normal-map  

## Blender

    Run blender.sh

## Blender DeepBump : 
https://github.com/HugoTini/DeepBump

Run this script to generate normalmap by deepbump
``` 
python3 dev-version/deepbump/batch_generate.py Inputs Outputs/DeepbumpNormalMap color_to_normals --color_to_normals-overlap LARGE --verbose
```

## NormalMap Online
Occlusion Map Generator
```js
cd dev-version/normalmap-online
npm install
node javascripts/main.js //the input and output paths are set at main.js file
```