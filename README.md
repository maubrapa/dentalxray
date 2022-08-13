# dentalxray
Detects pathologies and restorations.

### Requirements
The actual code was implemented and tested in Python 3.9.12.

### Labelme XML Parser
**labelMeXMLParser** directory presents the code that generates masks for image segmentation.

How is it organized:

	
~~~~
└── labelMeXMLParser
    ├── xml_parse.py: create masks
    ├── inputAnnotations: LabelMe xml annotation format
    ├── inputImages: sample images used for mask creation
    ├── outputCombined: output blended masks (input images + output visualization images)
    ├── outputMasks: training images (trimap like)
    └── outputMaskviz: color image mask for visualization
~~~~

<img src="https://user-images.githubusercontent.com/11092747/184506187-88298952-9d97-41a8-a12a-a03b99be0b3e.png" width="800">

### Segmentation code
`Coming soon`

### Dataset
<!-- The dataset used in this work with the corresponding ground truth data, as well as video sequences showing the results of our method, are publicly available at... -->
`Coming soon`

### Pre-trained models
`Coming soon`
