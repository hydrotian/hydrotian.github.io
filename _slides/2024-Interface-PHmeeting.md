---
marp: true
theme: default
paginate: true

style: |
  /* Title page styles */
  section.title {
    background: url('../images/slide_temp/title.png');
    background-size: cover;
    background-repeat: no-repeat;
    background-position: center;
  }

  section.title h1 {
    /* Custom style for h1 in title slides */
    color: rgb(200, 114, 46); /* Example color */
    font-size: 50px; /* Example font size */
    position: absolute;
    top: 180px;
    left: 120px;
    max-width: 32%;
    text-align: right;
  }

  section.title h2 {
    font-size: 20px; /* Example font size */
    position: absolute;
    top: 450px;
    right: 750px;
    max-width: 40%;
    text-align: right;
  }

  section.title h3 {
    font-size: 30px; /* Example font size */
    color: rgb(97, 98, 101); /* Example color */
    position: absolute;
    top: 550px;
    right: 750px;
    max-width: 40%;
    text-align: right;
  }

  /* Global styles */
  section {
    background-image: url('../images/slide_temp/bg.png');
    background-size: cover;
    background-repeat: no-repeat;
    background-position: center;
  }

  /* Style for h1 */
  h1 {
    position: absolute;
    top: 40px;
    left: 280px;
    font-size: 50px; /* Adjusts size based on the width of the viewport */
    max-width: 90%; /* Prevents the title from taking up the full width */
    color: rgb(200, 114, 46);
  }

  /* Style for h2, h3, and other text elements */
  h2, h3, h4, h5, h6, p, ul, ol, li {
    padding-left: 50px; /* This will move the text more or less to the right */
  }

  /* Style for two columns*/ 
  .columns {
    display: grid;
    grid-template-columns: repeat(2, minmax(0, 1fr));
    gap: 1rem;
    height: 400px;
  }

title: "Modeling Inter-Basin Water Transfers in E3SM"
collection: talks
date: 11/01/2024
location: "Online"
venue: "InteRFACE Monthly Permafrost Hydrology Meeting"
---

<!-- _class: title -->
<!-- _paginate: skip -->

# Modeling Inter-Basin Water Transfers in E3SM

## Tian Zhou, Matt Cooper, Chang Liao, Donghui Xu, Darren Engwirda, Ning Sun, Zeli Tan, Hong-Yi Li, Dongyu Feng, Gautam Bisht, and L. Ruby Leung
 

### 1/11/2024

---
# Background
- Saltwater intrusion in Delaware River Basin (DRB)
- What role Inter-Basin Water Transfer (IBT) is playing

[![Video Title](https://img.youtube.com/vi/EMBkJ-cDn8s/0.jpg)](https://www.youtube.com/watch?v=EMBkJ-cDn8s)

---
# IBT in Delaware River Basin

<div class="columns">
<div class="columns-left">

![image](../images/talks/2024/IBT_Delaware.png)

</div>
<div class="columns-right">

![image](../images/talks/2024/IBT_Delaware2.png)

<p style="text-align: center;">Up to 800 Million Gallons per Day (MGD) of water extracted for NYC through (IBT)
</p>

</div>
</div>

---

![width:1150px](../images/talks/2024/DRB_wateruse.png)

---
# A data-driven IBT scheme in MOSART-WM

<div class="columns">
<div class="columns-left">

![image](../images/talks/2024/p2p_IBT.png)

</div>
<div class="columns-right">

- Reservoir to reservoir transfer
- Monthly water transfer at each reservoir is provided by external files
- Mass is conserved 
- Limitations
  - No transfer loss
  - Instantaneous transfer
  - Consumptive use is not represented

</div>
</div>

---
![width:1100px](../images/talks/2024/Streamflow.png)

---

![width:900px](../images/talks/2024/SF_regression.png)

An empirical relationship (R2=0.71) between the weekly maximum salt front position (SF, km from the estuary) and the weekly minimum river discharge (Q, cfs) at Trenton, NJ can be established based on the long-term observation from DRBC:
          𝑆𝐹=278−4.4×log⁡(𝑄_𝑡 )−14.6×log⁡(𝑄_(𝑡−1) )

---
# IBT Leads to Enhanced Saltwater Intrusion
![images](../images/talks/2024/IBT_SF.png)
- IBT could push the maximum salt front location upstream by nearly 8 km 
- The findings also highlight the critical need to incorporate IBT into models that assess human impacts on large-scale hydrologic processes

---
<!-- _class: title -->
<!-- _paginate: skip -->

# Thank you!
---