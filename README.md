


## Installation




## Setup
This system and instructions will generally assume that you have set up this package as a stand-alone
python project, and that you have already set up the [oura-webhook-listener](https://github.com/BCM-Neurosurgery/oura-webhook-listener)
on a remote server (such as an AWS EC2 instance), the listener is subscribed to and receiving webhooks, and that the
server is accessible via SSH/SFTP.

If you need help setting up your EC2 instance to be accessible via SSH using a keyfile, we recommend you follow
[this tutorial](https://www.digitalocean.com/community/tutorials/how-to-configure-ssh-key-based-authentication-on-a-linux-server)

The first step is to copy the `stub-config.toml` file into a new file called `config.toml`, placed in the same 
directory. This file will provide all the information this package will need to run correctly. Since the `config.toml` 
can contain secure information like API and access keys, be sure to never push it to github.

The comments in the config file provide detailed information on what each value is responsible for. 

Several of the fields have meaningful defaults, that will work well if you've followed the default setup
instructions for the oura-webhook-listener. 
All the contents of the `[listener-ssh]` section must always be filled out, as these are the authentication details
used to open an SSH connection to the server.

## Details

### Data security considerations
This package uses HTTPS and SSH as communication protocols to transfer data. While these protocols are 
generally considered secure and are widely used, please check with the appropriate authority that these are sufficiently
secure for your use case.

This package also stores all the data as plaintext JSON files, so it is the responsibility of the user to 
ensure appropriate security practices are followed after the data is downloaded.

If you plan to scale you application to more than 10 users, you will need to work with Oura to
have your application verified and moved to production. 

### Downloading data


### Automating downloads
This package does not on it's own automate the data download process. It does, however, provide the make it very easy
to set up automation. 
