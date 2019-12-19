# oci-nigthly-stop
Stop your OCI instances at night.  And change the lisence models of your Autonomous Databases to BYOL.

# Supported instances for stop
- Compute Instances
- Autonomous Databases
- Database nodes of database systems (VM and Baremetal)

# Prerequisites
- oci python SDK
- Python 3 and above
- Pre-created oci-cli config file (~/.oci/config)  - you can create by oci setup config command

# How to use
1. Clone this repository.

2. Open stop.py file and edit # Specify your config file section accordingly.

3. `python3 stop.py` will start stopping transactions

4. Errors will be emitted to the standard output.  Redirect it to the file if you need record logs.

5. There is no scheduler included in the script. Please use cron or othe scheduler as you need. 
    - Exapmple of crontab entry to revoke every 0 am 
    ```
    0 * * * cd /home/opc; python3 -u /home/opc/oci-nightly-stop/stop.py > /home/opc/log/stop_date +%Y%m%d-%H%M%S.log 2>&1
    ```

6. If you want to exclude instances from stopping, set defined tags below for individual compute, db-systems or autnoumous database instances.
    - Tag Namespace : control
    - Defined tag ： nightly_stop
    - Tag value : false

Also guide for end users about taggin is avalable at https://github.com/mmarukaw/oci-nigthly-stop/blob/master/guide/howtoaddtags.md
(currently Japanese only)
