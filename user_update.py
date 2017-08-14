import argparse
import yaml
import umapi_client
import logging
from umapi_client import IdentityTypes, UserAction
from util import CSVAdapter

if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    parser = argparse.ArgumentParser(description='UNC User Converter')
    parser.add_argument('-c', '--config',
                        help='filename of config file',
                        metavar='filename', dest='config_filename')
    parser.add_argument('-u', '--users',
                        help='filename of user file',
                        metavar='filename', dest='users_filename')
    parser.add_argument('-t',
                        help='run updates in test mode',
                        dest='test_mode',
                        action='store_true',
                        default=False)

    args = parser.parse_args()

    with open(args.config_filename, "r") as f:
        config = yaml.load(f)
    conn = umapi_client.Connection(org_id=config["org_id"],
                                   auth_dict=config,
                                   test_mode=True,
                                   logger=logger)

    cols = ['Identity Type', 'Username', 'Domain', 'Email', 'First Name', 'Last Name', 'Country Code',
            'Product Configurations', 'Admin Roles', 'Product Configurations Administered']

    actions = {}
    for user_rec in CSVAdapter.read_csv_rows(args.users_filename, recognized_column_names=cols):
        user = UserAction(id_type=IdentityTypes.federatedID, email=user_rec['Email'])
        user.update(username=user_rec['Username'])
        res = conn.execute_single(user)
        logger.debug("Updating %s -- queued, sent, completed %s" % (user_rec['Email'], res))
        actions[user_rec['Email']] = user

    conn.execute_queued()

    for email, action in actions.items():
        if not action.execution_errors():
            logger.debug("%s - created successfully" % email)
        else:
            logger.debug("%s - ERROR - %s" % (email, action.execution_errors()))
