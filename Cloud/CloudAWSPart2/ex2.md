# Hosting a Static HTML Website on S3 and Serving It Through CloudFront

## Table of Contents
1. [Create a Simple Static HTML File](#create-a-simple-static-html-file)
2. [Host the Website on S3](#host-the-website-on-s3)
3. [Serve the Website Through CloudFront](#serve-the-website-through-cloudfront)

## 1. Create a Simple Static HTML File

- Create a new HTML file with your desired content (e.g., index.html).

## 2. Host the Website on S3

- Go to the AWS Management Console and navigate to the S3 service.
- Click on "Create bucket" and provide a unique bucket name.
- Choose 'ACLs enabled' -> Bucket owner preferred.
- Uncheck 'Block all public access' to make the bucket public.
- Upload your HTML file to the bucket and make it publicly accessible by configuring its permissions as follows:
  - Select the uploaded HTML file in the bucket.
  - Click on the "Actions" dropdown and choose "Make public."

## 3. Serve the Website Through CloudFront

- Go to the AWS Management Console and navigate to the CloudFront service.
- Click on "Create Distribution."
- Choose the "Web" distribution type.
- In the "Origin Settings" section, choose your S3 bucket as the "Origin Domain Name."
- In the "Default Cache Behavior Settings," keep the default settings.
- In the "Web Application Firewall (WAF)," choose "Do not enable security protections."
- In the "Distribution Settings," set the "Default root object - optional" to your desired file (e.g., index.html).
- Click "Create Distribution."
- After it, go to "Domain name" and copy the URL to see the file.

# Uploading and Downloading Files to/from S3 Using AWS CLI

## Table of Contents
1. [Install AWS CLI](#install-aws-cli)
2. [Create Access Key in AWS](#create-access-key-in-aws)
3. [Configure AWS CLI](#configure-aws-cli)
4. [Uploading a File to S3](#uploading-a-file-to-s3)
5. [Copying a File from S3 to Local Desktop](#copying-a-file-from-s3-to-local-desktop)

## 1. Install AWS CLI

- Install AWS CLI by running the following command in the terminal:
  ```
  sudo apt install awscli
  ```

## 2. Create Access Key in AWS

- Go to IAM -> Users -> Create Access Key to generate an access key.

## 3. Configure AWS CLI

- Run the following command in the local CLI to configure AWS CLI with the access key details:
  ```
  aws configure
  ```

## 4. Uploading a File to S3

- To upload a file to S3, use the following command:
  ```
  aws s3 cp /path/to/local/file s3://your-bucket-name/
  ```

## 5. Copying a File from S3 to Local Desktop

- To copy the file back from the bucket to your local desktop, use the following command:
  ```
  aws s3 cp s3://your-bucket-name/file /path/to/local/destination
  ```

# Adding a Download Feature to Your Weather Website

## Table of Contents
1. [Add a New Route in app.py](#add-a-new-route-in-app.py)
2. [Add the Download Button in weather.html](#add-the-download-button-in-weather.html)

## 1. Add a New Route in app.py

- Add a new route to your app.py that serves the image file. Create an endpoint named /download-sky-image and define the route to return the image as an attachment:
  ```python
  import os
  from flask import Flask, render_template, request, send_from_directory

  app = Flask(__name__)

  # ... (your existing code)

  # New route to serve the sky image
  @app.route('/download-sky-image')
  def download_sky_image():
      sky_image_url = 'https://bida-hosted-content.s3.eu-west-3.amazonaws.com/sky.png'
      filename = 'sky.png'
      response = requests.get(sky_image_url)
      return send_file(io.BytesIO(response.content), mimetype='image/png', as_attachment=True, attachment_filename=filename)

  if __name__ == '__main__':
      app.run()
  ```

## 2. Add the Download Button in weather.html

- In your weather.html template, add a link to the new endpoint that will trigger the download of the sky image when clicked:
  ```html
    <!-- New feature button to download the sky image -->
    <form action="/download-sky-image" method="get">
      <button type="submit">Download Sky Image</button>
    </form>
  ```

Now, when the user clicks the "Download Sky Image" link in the weather.html page, Flask will serve the image file from the S3 URL, and the user's browser will prompt them to download the image to their desktop.
