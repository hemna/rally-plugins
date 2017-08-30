My custom Rally dir.

How to use:
Have a working openstack env up and running
Install OpenStack Rally and create a new rally instance pointing to your openstack en.

Then:

git clone http://github.com/hemna/rally-plugins
mkdir ~/.rally
cd ~/.rally
ln -s ~/rally-plugins/plugins .

cd ~/rally-plugins
rally task start tasks/create-volume.json
