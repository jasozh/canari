# Canari
Canari is a GTK4/libadwaita app that tracks the enrollment status of Cornell classes. Requests are sent to Class Roster every 10 minutes, and updates are communicated through desktop notifications. If you need to add a class and are looking for a native Linux solution, this is the app for you.

<p align="center">
  <img src="https://user-images.githubusercontent.com/48730262/182104743-140e49fc-429f-4adb-8a12-7a9817a248d6.png">
</p>

## Installation
Canari is officially provided as a Flatpak. To install:
1. Visit https://flatpak.org/setup/ to set up Flatpak on your Linux distro
2. Go to `Releases` and download the Flatpak of the latest stable version
3. Install Canari via the command line with `flatpak install com.github.jasozh.Canari.flatpak` or by using a GUI software center

There are currently no plans to host a Flatpak repository. You can check this page periodically to download new releases.

## Building
The recommended way to build Canari is through GNOME Builder. Visit the guide https://wiki.gnome.org/Newcomers/BuildProject to get started.
