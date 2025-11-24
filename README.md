# Adrian Caballero Cloud Resume
## [Website Link](https://www.aeglero.com "Adrian Caballero Website")
![alt text](https://github.com/adrianbcaballero/acaballero-cloud-resume/raw/main/docs/CloudResume.png "Architecture Diagram")

## Table of Contents

- [Adrian Caballero Cloud Resume](#adrian-caballero-cloud-resume)
  - [Table of Contents](#table-of-contents)
  - [Cloud Resume Challenge Overview](#cloud-resume-challenge-overview)
  - [Challenge Steps](#challenge-steps)
    - [1. Certification](#1.-certification)
    - [2. Front End Website](#2.-front-end-website)
      - [2.1. HTML](#2.1.-html)
      - [2.2. CSS](#2.2.-css)
      - [2.3. S3 Website](#2.3.-s3-website)
      - [2.4. HTTPS](#2.4.-static-assets)
      - [2.5. DNS](#2.5.-cloudfront)
    - [3. Back End API](#3.-back-end-api)
      - [3.1. Python](#3.1.-python)
      - [3.2. Database](#3.2.-database)
      - [3.3. API](#3.3.-api)
      - [3.4. JavaScript](#3.4.-javascript)
    - [4. Automation / CI](#4.-automation-/-ci)
      - [4.1. Infrastructure as Code](#4.1.-infrastructure-as-code)
      - [4.2. Source Control](#4.2.-source-control)
      - [4.3. CI/CD](#4.3.-ci/cd)
    - [5. Journey Documentation](#5.-journey-documentation)
      - [5.1. Blog Post](#5.1.-blog-post)


## Cloud Resume Challenge Overview

The Cloud Resume Challenge was a challenge created by Forrest Brazeal to enhance participants' knowledge and experience with the cloud. It's a multi-step resume project that helps build and demonstrate skills fundamental to pursuing a career in the cloud.
[Original challenge](https://cloudresumechallenge.dev/ "Original Challenge Link")

## Challenge Steps

### 1. Certification

The first step was getting certified. The foundational AWS Certified Cloud Practitioner taught me AWS Cloud concepts, AWS services, security, architecture, pricing, and support to build my AWS Cloud knowledge, which was helpful throughout the challenge.

### 2. Front End Website

#### 2.1. HTML
The core structure of the resume was created using HTML.

#### 2.2. CSS
CSS was used to style and enhance the visual appearance and user experience of the website.

#### 2.3. S3 Website
All the front-end files necessary for the resume were deployed online using an AWS S3 bucket with static website hosting. The files include those in the front end folder which were HTML, CSS, and JavaScript.

#### 2.4. HTTPS
To secure the website, CloudFront was configured to enable HTTPS.

#### 2.5. DNS
Route 53 was used to set up custom DNS domain mapping, which directed traffic to the CloudFront distributions with an easy-to-remember domain name.

### 3. Back End API

#### 3.1. Python
I created and implemented two Lambda functions using Python to handle backend logic and processing using Terraform. The first lambda function was made with a trigger on the branch content S3 bucket. When changes were detected it would copy the new files to the actual S3 website bucket. Along with that, it would use CloudWatch to log the actions and also send a SNS email notification alerting the developer about the changes. The second lambda function had a trigger set to the REST API gateway on the static website. When a request was made, which was each time the website was accessed, it would update the DynamoDB to the new view count value and return the new value back.

#### 3.2. Database
The database used was DynamoDB, a fully managed NoSQL database service provided by AWS. It was created using Terraform and was used to store the access count of the website. 

#### 3.3. API
The REST API gateway was used to accept requests from the web app to trigger a lambda function to update the DynamoDB value. It also returned the updated value to the front end.

#### 3.4. JavaScript
JavaScript was used in conjunction with the API to activate the lambda function when a user accessed the website.

### 4. Automation / CI

#### 4.1. Infrastructure as Code
Infrastructure as Code (IaC) was implemented using Terraform templates to define and provision AWS resources. Although the first beginning of the project began in the AWS console, the following were made using Terraform: DynamoDB, both Lambda Functions, API Gateway, SNS topic, the front end branch S3 bucket, and CloudWatch logs. The approach made for easier resource management and deployment consistency.

#### 4.2. Source Control
Git and GitHub Actions were used for source control management, enabling version tracking and codebase management throughout the project.

#### 4.3. CI/CD
GitHub Actions served as the CI/CD pipeline. The workflows ran a Terraform plan when a pull request was created, and when the commits were pushed, a Terraform Apply was made with any new updates.

### 5. Development Process

#### 5.1. Blog Post
A detailed blog post is in the process of being written that documented my entire journey, experiences, challenges faced, and lessons learned. Stay tuned to read about my journey through the challenge on my blog post!