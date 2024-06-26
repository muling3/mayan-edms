from django.utils.encoding import force_bytes, force_str

from .literals import TEST_EMAIL_BASE64_FILENAME


class MockIMAPMessage:
    def __init__(self, body, uid):
        self.flags = set()
        self.mailbox = None
        self.uid = uid
        self.body = body

    def flags_add(self, flags_string):
        for flag_string in flags_string.split():
            # Remove parenthesis.
            flag_string = flag_string[1:-1]
            self.flags.add(flag_string)

    def flags_remove(self, flags_string):
        for flag_string in flags_string.split():
            # Remove parenthesis.
            flag_string = flag_string[1:-1]
            self.flags.discard(flag_string)

    def flags_set(self, flags_string):
        self.flags = set()
        for flag_string in flags_string.split():
            # Remove parenthesis.
            flag_string = flag_string[1:-1]
            self.flags.add(flag_string)

    def delete(self):
        self.mailbox.messages.pop(self.uid)

    def get_flags(self):
        return ' '.join(self.flags)

    def get_number(self):
        return list(
            self.mailbox.messages.values()
        ).index(self)


class MockIMAPMailbox:
    def __init__(self, name='INBOX'):
        self.messages = {}
        self.name = name

    def get_message_by_number(self, message_number):
        message_list = list(
            self.messages.values()
        )

        return message_list[message_number - 1]

    def get_message_by_uid(self, uid):
        uid = force_str(s=uid)
        return self.messages[uid]

    def get_message_count(self):
        return len(self.messages)

    def get_messages(self):
        return list(
            self.messages.values()
        )

    def messages_add(self, body, uid):
        self.messages[uid] = MockIMAPMessage(body=body, uid=uid)
        self.messages[uid].mailbox = self


class MockIMAPServer:
    def __enter__(self):
        return self

    def __exit__(self, *args, **kwargs):
        self.logout()
        self.close()

    def __init__(self):
        self.mailboxes = {
            'INBOX': MockIMAPMailbox(name='INBOX')
        }
        self.mailbox_selected = None

    def _add_test_message(self, content=None, uid=None):
        body = content or TEST_EMAIL_BASE64_FILENAME

        uid = uid or str(
            len(
                self.mailboxes['INBOX'].messages
            )
        )

        body = force_bytes(s=body)

        self.mailboxes['INBOX'].messages_add(body=body, uid=uid)

    def _fetch(self, messages):
        flag = '\\Seen'
        flag_modified = []
        message_number_list = []
        results = []
        uids = []

        for message in messages:
            if flag not in message.flags:
                message.flags_add(flag)
                flag_modified.append(message)

            message_number = message.get_number()
            message_number_list.append(
                force_str(s=message_number)
            )
            uid = message.uid
            uids.append(uid)
            body = message.body

            results.append(
                (
                    '{} (UID {} RFC822 {{{}}}'.format(
                        message_number, uid, len(body)
                    ), body
                )
            )

        results.append(
            ' FLAGS ({}))'.format(flag),
        )
        results.append(
            '{} (UID {} FLAGS ({}))'.format(
                ' '.join(message_number_list), ' '.join(uids), flag
            )
        )
        return results

    def close(self):
        return (
            'OK', ['Returned to authenticated state. (Success)']
        )

    def expunge(self):
        result = []

        for message in self.mailbox_selected.get_messages():
            if '\\Deleted' in message.flags:
                result.append(
                    force_str(
                        s=message.get_number()
                    )
                )
                message.delete()

        return (
            'OK', ' '.join(result)
        )

    def fetch(self, message_set, message_parts):
        messages = []

        for message_number in message_set.split():
            messages.append(
                self.mailbox_selected.get_message_by_number(
                    message_number=int(message_number)
                )
            )

        return (
            'OK', self._fetch(messages=messages)
        )

    def login(self, user, password):
        return (
            'OK', [
                '{} authenticated (Success)'.format(user)
            ]
        )

    def logout(self):
        return (
            'BYE', ['LOGOUT Requested']
        )

    def search(self, charset, *criteria):
        """
        7.2.5.  SEARCH Response
        Contents:   zero or more numbers
        The SEARCH response occurs as a result of a SEARCH or UID SEARCH
        command.  The number(s) refer to those messages that match the
        search criteria.  For SEARCH, these are message sequence numbers;
        for UID SEARCH, these are unique identifiers.  Each number is
        delimited by a space.

        Example:    S: * SEARCH 2 3 6
        """
        results = [
            self.mailbox_selected.messages[0]
        ]

        message_sequences = []
        for message in results:
            message_sequences.append(
                force_str(
                    s=message.get_number()
                )
            )

        return (
            'OK', ' '.join(message_sequences)
        )

    def select(self, mailbox='INBOX', readonly=False):
        self.mailbox_selected = self.mailboxes[mailbox]

        return (
            'OK', [
                self.mailbox_selected.get_message_count()
            ]
        )

    def store(self, message_set, command, flags):
        results = []

        for message_number in message_set.split():
            message = self.mailbox_selected.messages[
                int(message_number) - 1
            ]

            if command == 'FLAGS':
                message.flags_set(flags_string=flags)
            elif command == '+FLAGS':
                message.flags_add(flags_string=flags)
            elif command == '-FLAGS':
                message.flags_remove(flags_string=flags)

            results.append(
                '{} (FLAGS ({}))'.format(
                    message_number, message.get_flags()
                )
            )

        return ('OK', results)

    def uid(self, command, *args):
        if command == 'FETCH':
            uid = args[0]
            messages = [
                self.mailbox_selected.get_message_by_uid(uid=uid)
            ]
            return (
                'OK', self._fetch(messages=messages)
            )
        elif command == 'STORE':
            results = []
            uid = args[0]
            subcommand = args[1]
            flags = args[2]
            message = self.mailbox_selected.get_message_by_uid(uid=uid)

            if subcommand == 'FLAGS':
                message.flags_set(flags_string=flags)
            elif subcommand == '+FLAGS':
                message.flags_add(flags_string=flags)
            elif subcommand == '-FLAGS':
                message.flags_remove(flags_string=flags)

            results.append(
                '{} (FLAGS ({}))'.format(
                    uid, message.get_flags()
                )
            )
            return ('OK', results)
        elif command == 'SEARCH':
            try:
                message = self.mailbox_selected.get_message_by_number(
                    message_number=1
                )
            except IndexError:
                message_sequences = ()
            else:
                message_sequences = (message.uid,)

            return (
                'OK', [
                    ' '.join(message_sequences)
                ]
            )


class MockPOP3Mailbox:
    """RFC 1725"""
    _message_index_base = 1
    message_list = []

    # Don't add __enter__ and __exit__ attributes. The Python poplib library
    # does not support opening as a context.

    def _add_test_message(self, content=None):
        content = content or TEST_EMAIL_BASE64_FILENAME
        self.message_list.append(
            [
                force_bytes(s=content)
            ]
        )

    def dele(self, which):
        return self.message_list.pop(which - self._message_index_base)

    def getwelcome(self):
        return force_bytes(
            s='+OK server ready for requests from 127.0.0.0 xxxxxxxxxxxxxxxxx'
        )

    def list(self, which=None):
        # (b'+OK 7 messages (304882 bytes)',
        # [b'1 4800',
        #  b'2 16995',
        #  b'3 12580',
        #  b'4 196497',
        #  b'5 48900',
        #  b'6 12555',
        #  b'7 12555'],
        #  63)

        result = []
        result_entry_number = self._message_index_base
        result_total_size = 0

        for value in self.message_list:
            entry_size = 0
            for line in value:
                entry_size = entry_size + len(line)

            result_total_size += entry_size
            result.append(
                force_bytes(
                    s='{} {}'.format(result_entry_number, entry_size)
                )
            )

            result_entry_number = result_entry_number + 1

        # Sum the line sizes in bytes plus 2 (CR+LF)
        result_size = sum(
            [
                len(entry) + 2 for entry in result
            ]
        )

        return (
            force_bytes(
                s='+OK {} messages ({} bytes)'.format(
                    len(self.message_list), result_total_size
                )
            ), result, result_size
        )

    def user(self, user):
        return force_bytes(s='+OK send PASS')

    def pass_(self, pswd):
        return force_bytes(s='+OK Welcome.')

    def quit(self):
        return

    def retr(self, which):
        return (
            None, self.message_list[which - self._message_index_base], None
        )
