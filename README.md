## Covid_Portal

# Summary
  The development of vaccines and immunotherapies requires integration of data from a variety of fields including structural biology, immunology, virology and genetics. The Protein Explorer Tool (PET) aims to combine these data into a single interface that researchers can use to identify connections between structural, phenotypic and immunological properties.

  The tool displays three panels with pre-selected data for spike protein sequences, epitope sequences and structure sequences. Additional records can be added by opening up the filter panel at the bottom of the screen. 
  
 Data presented in this portal was extracted from biological databases using a pipeline, as detailed here - https://miro.com/welcomeonboard/TlvADlGy1rABZmGP80hEOWZxj2j5lBCiJwiU8M93XnlnP0x8Ld3tnlw96y50Q9D7. 

 Details of the design including features available can be found here - https://docs.google.com/document/d/12FJT-hlBNhEi9mACm87F-cw1OKui7wiCqAqV7H1PWC0/edit?usp=sharing. 

 A loom video that shows how the portal can be used can be found here - https://www.loom.com/share/4869728369b44c14a9b7d2de5647bac2. 
  
 Data in each panel can be sorted by fields available on lists in the top right of each panel. For the epitope panel, there is also a sort feature on the top left, that allows for a higher level sort, as described in the design document. In each filter panel, table data can be sorted and filters are provided for each column.
  
# Framework used
  The project is built using Python 3.5+ and Angular-Cli version 9.5.0 and node version 13.13.0.
  
# Deployment instructions
  There are two sub-folders - one corresponding to the angular frontend (covidPortalFrotnEnd) and the other Python backend (webCovidPortal). Each can be started using Docker.
  
  For angular, to launch the app, using docker - 
  - sudo docker build --no-cache -t portal-angular .
  - sudo docker run -p 80:80 portal-angular
  
  For Django, to launch the app, using docker - 
  - sudo docker build --no-cache -t portal-django .
  - sudo docker run -p 8000:80
  
  The Django API is available as a service from 
  - http://portaldb.stage.coronawhy.org/
