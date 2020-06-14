# When files are made in docker the permissions get all messed up
# instead of fixing that issue since its work
# lets just make current user the owner
user=$(id -g)
sudo chown -R $user:$user .  


# These commands will allow the docker group to always have access to the files
# chgrp -R docker ./<FOLDER>
# chmod g+rwX ./<FOLDER> -R