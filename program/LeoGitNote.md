# Git notes

## First time github git terminal setup

Your first time with git and github
If you’ve never used git or github before, there are a bunch of things that you need to do. It’s very well explained on github, but repeated here for completeness.

Get a github account.
Download and install git.
Set up git with your user name and email.

Open a terminal/shell and type:

$ git config --global user.name "Your name here"
$ git config --global user.email "your_email@example.com"
(Don’t type the $; that just indicates that you’re doing this at the command line.)

I also do:

$ git config --global color.ui true
$ git config --global core.editor emacs
The first of these will enable colored output in the terminal; the second tells git that you want to use emacs.

Set up ssh on your computer. I like Roger Peng’s guide to setting up password-less logins. Also see github’s guide to generating SSH keys.

Look to see if you have files ~/.ssh/id_rsa and ~/.ssh/id_rsa.pub.
If not, create such public/private keys: Open a terminal/shell and type:

$ ssh-keygen -t rsa -C "your_email@example.com"
Copy your public key (the contents of the newly-created id_rsa.pub file) into your clipboard. On a Mac, in the terminal/shell, type:

$ pbcopy < ~/.ssh/id_rsa.pub
Paste your ssh public key into your github account settings.

Go to your github Account Settings
Click “SSH Keys” on the left.
Click “Add SSH Key” on the right.
Add a label (like “My laptop”) and paste the public key into the big text box.
In a terminal/shell, type the following to test it:

$ ssh -T git@github.com
If it says something like the following, it worked:

Hi username! You've successfully authenticated, but Github does
not provide shell access.

## Upload large files to github

In mac:

```bash
brew install git-lfs
git lfs install
git lfs track "*.7z*"
git add .gitattributes ---ignore this step for github, otherwise github would ask for lfs quota.
git add .
git commit -m "Add large file"
git push origin main
```
Github limits the size of each file to less than 2GB. So that files larger than 2GB should be split into multiple volumes. 
In mac, you can use Keka to split and zip the files.

# References

* https://kbroman.org/github_tutorial/pages/first_time.html
* https://www.digitalocean.com/community/tutorials/fork-clone-make-changes-push-to-github
* https://git-lfs.github.com/

