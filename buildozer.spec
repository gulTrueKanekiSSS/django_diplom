[app]
# (str) Title of your application
title = SmartInventory

# (str) Package name
package.name = myapp

# (str) Package domain (needed for android/ios packaging)
package.domain = org.example

# (str) Source code where the main.py is located
source.dir = ./kivy_application/

# (list) Source files to include (let empty to include all the files)
source.include_exts = py,png,jpg,kv,atlas
source.include_patterns = cacert.pem
# (str) Application versioning (method 1)
version = 1.2


# (list) Application requirements
# Please ensure that you have the proper version of torch for mobile compatibility.
requirements = python3,kivy,requests,opencv-python-headless,torch,cython,numpy,certifi

# (str) Path to the main application file
entrypoint = .buildozer/android/app/main.py

# (str) Presplash of the application
# presplash.filename = %(source.dir)s/data/presplash.png

# (str) Icon of the application
# icon.filename = %(source.dir)s/data/icon.png

# (list) Permissions
android.permissions = INTERNET,CAMERA

[buildozer]
# (int) Log level (0, 1, 2)
log_level = 2

# (str) Path to build artifact storage, absolute or relative to spec file
# bin_dir = ./bin

# (str) Path to package project storage, absolute or relative to spec file
# package_data_dir = ./package_data

# (str) Android NDK version to use. Required to be '23b' or '25b'
android.ndk = 23b

[android]
# (str) Title of your application
title = MyApp

# (str) Package name
package.name = myapp

# (str) Package domain (needed for android/ios packaging)
package.domain = org.example

# (int) Target Android API, should be as high as possible.
android.api = 33

# (int) Minimum API your APK will support.
android.minapi = 21
