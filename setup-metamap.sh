#!/bin/sh
sed 's/^read/##/g' bin/install.sh > bin/install_ncats.sh
chmod +x bin/install_ncats.sh
sh /metamap/public_mm/bin/install_ncats.sh
