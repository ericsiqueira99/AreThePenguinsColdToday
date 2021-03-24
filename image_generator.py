from simple_image_download import simple_image_download as simp

response = simp.simple_image_download
words_to_search = 'penguins'
amount_of_pics = 365
response().download(words_to_search, amount_of_pics)