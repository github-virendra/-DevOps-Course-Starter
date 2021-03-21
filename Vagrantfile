# -*- mode: ruby -*-
# vi: set ft=ruby :

# All Vagrant configuration is done below. The "2" in Vagrant.configure
# configures the configuration version (we support older styles for
# backwards compatibility). Please don't change it unless you know what
# you're doing.
Vagrant.configure("2") do |config|
  config.vm.box = "hashicorp/bionic64"
  config.vm.network "forwarded_port", guest: 5000, host: 5000

  # To manage your Python environment, you'll use pyenv. Pyenv is a popular tool for
  # managing multiple python versions on a single machine. This installation should be
  # a provisioning script in the Vagrantfile. That way, vagrant will handle running the
  # script when a new VM is created.
  config.vm.provision "shell", privileged: false, inline: <<-SHELL
    sudo apt-get update
    
    # TODO: Install pyenv prerequisites
    sudo apt-get install -y build-essential libssl-dev zlib1g-dev libbz2-dev \
    libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev libncursesw5-dev \
    xz-utils tk-dev libffi-dev liblzma-dev python-openssl git
    
    # TODO: Install pyenv
    git clone https://github.com/pyenv/pyenv.git ~/.pyenv

    echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.profile
    echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.profile
    echo -e 'if command -v pyenv 1>/dev/null 2>&1; then\n  eval "$(pyenv init -)"\nfi' >> ~/.profile
    
    source ~/.profile
    
    pyenv install 3.9.0

    pyenv global 3.9.0

    curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python 

    
  SHELL

  config.trigger.after :up do |trigger|
    trigger.name = "Launching App"
    trigger.info = "Running the TODO app setup script"
    trigger.run_remote = {privileged: false, inline: "
    
    # Install dependencies and launch
    cd /vagrant
    pwd
    poetry install
    
    nohup poetry run flask run --host=0.0.0.0 > logs.txt 2>&1 &

    "}
  end
end
