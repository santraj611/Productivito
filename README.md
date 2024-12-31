### Productivito

Productivito is productivity tool. Which helps you moniter and Analyse your pc uses and gives you insights
By graphs, Which can be categorised by monthly or weekly uses.

### Current Known Bugs:
- Make the database file be stored in some safe location.

### Improvment Thoughts:
- Update the graph page for total usage and today usage
- Dockerize it
- Make a logging machanism
- Desine GUI for it.
- use ShadCNui
- Make it Self-Hostable.

### Requiremants
For graphs you need `matplotlib`, Which can be installed using `pip3`
```
pip3 install matplotlib
pip3 install flask
pip3 install psutil

```

### How to make it auto start at startup
For Linux:
Make a `.desktop` file inside your autostart config folder if it does not exit make one.
```
mkdir ~/.config/autostart/
```
And then make a `Productivito.desktop` file for the Productivito app to make it autostart everytime you start your pc.
```
[Desktop Entry]
Type=Application
Name=Productivito
Exec=/bin/bash /path/to/your/autostart.sh
Terminal=flase
Comment=PC Usage Tracker
X-GNOME-Autostart-enabled=true
```
Note: Make sure you replace `/path/to/your/autostart.sh` with your location of script in your pc.
Also note that you need to make the script executable.
```
chmod +x /path/to/script
```
You can also create a link to `autostart.sh` file and make that run:
```bash
ln -s /path/to/autostart.sh ~/.config/autostart/
```
