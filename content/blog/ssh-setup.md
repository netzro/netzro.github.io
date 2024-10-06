---
Title: Setting Up SSH Keys for a VPS
Date: 2024-10-04
Tags: 100DaysToOffload, linux
---

## Introduction

Using SSH keys to access your Virtual Private Server (VPS) is one of the most secure methods of authentication. SSH keys provide a stronger layer of security compared to password logins by utilizing a cryptographic key pair. This guide will walk you through generating SSH keys, copying them to your server, and disabling password logins to enhance security.

---

## Step 1: Generate SSH Keys

Before you can use SSH key-based authentication, you need to generate an SSH key pair on your local machine.

1. Open a terminal on your local machine.
2. Run the following command to generate an SSH key pair:

    ```bash
    ssh-keygen -t rsa -b 4096
    ```

    This will generate a 4096-bit RSA key, which is secure and recommended for most uses.

3. When prompted to enter a file in which to save the key, press `Enter` to accept the default location (`~/.ssh/id_rsa`).

4. You can also set a passphrase for additional security, or press `Enter` to skip this step if you don’t want a passphrase.

---

## Step 2: Copy the SSH Key to Your VPS

Once your key pair is generated, you need to copy the public key to your VPS so it knows to trust your key when you try to log in.

1. Use the following command to copy your public key to the VPS:

    ```bash
    ssh-copy-id your_user@your_vps_ip_address
    ```

    Make sure to replace `your_user` with the actual username on your VPS (if you don’t have a user yet, create one with `adduser`). Also, replace `your_vps_ip_address` with the actual IP address of your VPS.

2. If `ssh-copy-id` is not available, you can manually copy the public key by doing the following:
    - Display your public key on your local machine:

        ```bash
        cat ~/.ssh/id_rsa.pub
        ```

    - Log into your VPS using your password and open the authorized keys file:

        ```bash
        ssh your_user@your_vps_ip_address
        mkdir -p ~/.ssh
        nano ~/.ssh/authorized_keys
        ```

    - Paste the public key into this file, save it, and exit.

    - Set the correct permissions for the `.ssh` directory and the `authorized_keys` file:

        ```bash
        chmod 700 ~/.ssh
        chmod 600 ~/.ssh/authorized_keys
        ```

---

## Step 3: Disable Password Authentication

After ensuring that you can log in using SSH keys, it's a good security practice to disable password-based authentication.

1. Open the SSH configuration file on your VPS:

    ```bash
    sudo nano /etc/ssh/sshd_config
    ```

2. Find the following directives and change them as shown:

    ```bash
    PasswordAuthentication no
    PermitRootLogin no
    ```

    This disables password login and root login, making your server more secure.

3. Save the file and exit the editor.

4. Restart the SSH service to apply the changes:

    ```bash
    sudo systemctl restart ssh
    ```

---

## Step 4: Test SSH Key Login

Before logging out of your current session, open a new terminal window and test the SSH key login:

```bash
ssh your_user@your_vps_ip_address
