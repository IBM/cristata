# Vagrant file for Cristata
#
# installs ibm cloud command line tools
# installs build dependenices for python 3.6.4
# installs python 3.6.4


$provision_root = <<'SCRIPT_ROOT'
add-apt-repository ppa:deadsnakes/ppa
apt-get update
apt-get upgrade -y

# for building Python 3.6.4
apt-get install -y openjdk-8-jdk maven zip python3.6 python3-pip jq flake8
apt-get autoremove -y

cd ${HOME}

echo "fetch, install bluemix cli"
wget -q http://public.dhe.ibm.com/cloud/bluemix/cli/bluemix-cli/0.7.1/IBM_Cloud_CLI_0.7.1_amd64.tar.gz -O ./Bluemix_CLI.tar.gz
tar -xf Bluemix_CLI.tar.gz
cd Bluemix_CLI
./install_bluemix_cli
cd ..
rm Bluemix_CLI.tar.gz
rm -rf Bluemix_CLI

SCRIPT_ROOT


$provision_user = <<'SCRIPT_USER'

bx plugin install cloud-functions -r Bluemix

# add some variables to ~/.bashrc
cat <<'EOF_BASHRC' > $HOME/.bashrc

cd /vagrant

EOF_BASHRC

SCRIPT_USER


Vagrant.configure("2") do |config|
  config.vm.box = "ubuntu/xenial64"

  config.vm.provision :shell, inline: $provision_root
  config.vm.provision :shell, privileged: false, inline: $provision_user

  config.vm.provider "virtualbox" do |vb|
    vb.customize ["modifyvm", :id, "--name", "cristata"]
    vb.customize ["modifyvm", :id, "--cpus", "2"]
    vb.customize ["modifyvm", :id, "--cpuexecutioncap", "90"]
    vb.customize ["modifyvm", :id, "--memory", "2048"]
  end

  config.vm.hostname = "cristata"

end
