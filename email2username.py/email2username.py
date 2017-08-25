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
    parser = argparse.ArgumentParser(description='Federated ID Convert from Email to Username Tool')
    parser.add_argument('-c', '--config', required=True, type=argparse.FileType('r'),
                        help='path to config file containing integration credentials',
                        metavar='config.yml', dest='config_filename')
    parser.add_argument('-u', '--users', required=True, type=argparse.FileType('r'),
                        help='path to csv spreadsheet with columns Username, Email',
                        metavar='users.csv', dest='users_filename')
    parser.add_argument('-t', '--test-mode',
                        help='run updates in test mode (no changes made)',
                        dest='test_mode', action='store_true', default=False)
    parser.add_argument('-r', '--reverse',
                        help='reverse conversion (set username to email)',
                        dest='from_email', action='store_false', default=True)

    args = parser.parse_args()

    with open(args.config_filename, "r") as f:
        config = yaml.load(f)
    conn = umapi_client.Connection(org_id=config["org_id"],
                                   auth_dict=config,
                                   test_mode=args.test_mode,
                                   logger=logger)

    cols = ['Username', 'Email']

    actions = {}
    for user_rec in CSVAdapter.read_csv_rows(args.users_filename, recognized_column_names=cols):
        username, email = user_rec.get('Username'), user_rec.get('Email')
        if not username or not email:
            logger.warning("Skipping input record with missing Username and/or Email: %s" % user_rec)
            continue
        user = UserAction(id_type=IdentityTypes.federatedID, email=email)
        if args.from_email:
            user.update(username=username)
            actions[email] = user
        else:
            user.update(username=email)
            actions[username] = user
        conn.execute_single(user)

    conn.execute_queued()

    successes, failures = 0, 0
    for key, action in actions.items():
        if not action.execution_errors():
            successes += 1
        else:
            failures += 1
            logger.error("Conversion of %s failed: %s" % (key, action.execution_errors()))
    logger.info("Conversions attempted/succeeded/failed: %d/%d/%d" % (len(actions), successes, failures))
