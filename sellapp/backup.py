

def license_check(request, args):
    print()
    print()
    print('license_check')

    try:
        args_decrypted = decrypt(args.encode(), public_fernet)
    except InvalidToken:
        return HttpResponse('error')

    args = args_decrypted.split('/')
    username, license_key, bios_sn, csproduct, mac_id, system, version, processor, model, app_version = args

    try:

        print('license_key', license_key)
        print(License.objects.first().key)

        license = License.objects.get(key=license_key)
        if license.user.username != username:
            print('License username doesnt match')
            return HttpResponse(
                'This username or license pair doesn\'t exist.')

        allowed_machines = license.machine_set.all().filter(
            is_blacklisted=False)

        hardware_id = f'{bios_sn}, {csproduct}, {mac_id}'
        info = f'{system} {version}, {processor}'
        current_machine = None

        try:
            print('Trying to find existing machine')
            # If it's existing machine, update last login time
            current_machines = allowed_machines.order_by('-last_login')
            current_machines = allowed_machines.filter(hardware_id=hardware_id)
            current_machine = current_machines.first()
            current_machine.update_last_login_time()
            print('Found machine')
            print('hardware_id', hardware_id)
            print('info', info)
            print('model', model)

        except Exception as e:
            print('No machine found')
            print(e)
            pass

        try:
            if current_machine is None:
                print('Creating new machine')
                if len(allowed_machines) < license.max_machines_limit:
                    print('Under limit')
                    new_machine = Machine()
                    new_machine.create_machine(hardware_id, info, model, False,
                                               license)
                current_machine = new_machine

                print('hardware_id', hardware_id)
                print('info', info)
                print('model', model)
                print('Created new machine!')
        except Exception as e:
            print('Too many machines')
            return HttpResponse(
                'Maximum machines limit reached on this account.')

        if current_machine is not None:
            print('OK!')
            return HttpResponse('ok')

    except (License.DoesNotExist, Machine.DoesNotExist) as e:
        print('License does not exist')
        pass

    print('No license found: ERROR')

    return HttpResponse(
        'License not found, maximum machines limit is reached, or machines is blacklisted by an owner of a license.'
    )


def decrypt_code_with_license(request, args):
    print()
    print()
    print('decrypt_code_with_license')

    try:
        args_decrypted = decrypt(args.encode(), public_fernet)
    except InvalidToken:
        return HttpResponse('error')

    args = args_decrypted.split('/')
    username, license_key, bios_sn, csproduct, mac_id, system, version, processor, model, encrypted_code, app_version = args

    try:

        print('license_key', license_key)
        print(License.objects.first().key)

        license = License.objects.get(key=license_key)
        if license.user.username != username:
            print('License username doesnt match')
            return HttpResponse(
                'This username or license pair doesn\'t exist.')

        allowed_machines = license.machine_set.all().filter(
            is_blacklisted=False)

        hardware_id = f'{bios_sn}, {csproduct}, {mac_id}'
        info = f'{system} {version}, {processor}'
        current_machine = None

        try:
            print('Trying to find existing machine')
            # If it's existing machine, update last login time
            current_machines = allowed_machines.order_by('-last_login')
            current_machines = allowed_machines.filter(hardware_id=hardware_id)
            current_machine = current_machines.first()
            current_machine.update_last_login_time()
            print('Found machine')
            print('hardware_id', hardware_id)
            print('info', info)
            print('model', model)

        except Exception as e:
            print('No machine found')
            print(e)
            pass

        try:
            if current_machine is None:
                print('Creating new machine')
                if len(allowed_machines) < license.max_machines_limit:
                    print('Under limit')
                    new_machine = Machine()
                    new_machine.create_machine(hardware_id, info, model, False,
                                               license)
                current_machine = new_machine

                print('hardware_id', hardware_id)
                print('info', info)
                print('model', model)
                print('Created new machine!')
        except Exception as e:
            print('Too many machines')
            return HttpResponse(
                'Maximum machines limit reached on this account.')

        if current_machine is not None:
            print('Decrypt code')
            decrypted_code = decrypt_code(app_version, encrypted_code)
            return HttpResponse(decrypted_code)

    except (License.DoesNotExist, Machine.DoesNotExist) as e:
        print('License does not exist')
        pass

    print('No license found: ERROR')

    return HttpResponse(
        'License not found, maximum machines limit is reached, or machines is blacklisted by an owner of a license.'
    )