from google_images_download import google_images_download

donwloader = google_images_download.googleimagesdownload()
arguments = {"keywords":"Polar bears,baloons,Beaches","limit":5,"print_urls":True}
paths = donwloader.download(arguments)
print(paths)