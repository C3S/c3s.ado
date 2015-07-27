# For copyright and license terms, see COPYRIGHT.rst (top level of repository)
# Repository: https://github.com/C3S/c3s.ado

repositories = (
    # (
    #     git repository url or None.
    #     git clone option, required if repository is given.
    #     relative path to create or clone.
    # ),
    (
        None,
        None,
        'postgresql-data'
    ),
    (
        None,
        None,
        'ado/var/lib/trytond'
    ),
    (
        'https://github.com/tryton/trytond.git',
        '--branch=3.4',
        'ado/src/trytond'
    ),
    (
        'https://github.com/tryton/country.git',
        '--branch=3.4',
        'ado/src/country'
    ),
    (
        'https://github.com/tryton/currency.git',
        '--branch=3.4',
        'ado/src/currency'
    ),
    (
        'https://github.com/tryton/party.git',
        '--branch=3.4',
        'ado/src/party'
    ),
    (
        'https://github.com/tryton/company.git',
        '--branch=3.4',
        'ado/src/company'
    ),
    (
        'https://github.com/tryton/product.git',
        '--branch=3.4',
        'ado/src/product'
    ),
    (
        'https://github.com/tryton/account.git',
        '--branch=3.4',
        'ado/src/account'
    ),
    (
        'https://github.com/tryton/account_product.git',
        '--branch=3.4',
        'ado/src/account_product'
    ),
    (
        'https://github.com/tryton/account_invoice.git',
        '--branch=3.4',
        'ado/src/account_invoice'
    ),
    (
        'https://github.com/tryton/account_invoice_line_standalone.git',
        '--branch=3.4',
        'ado/src/account_invoice_line_standalone'
    ),
    (
        'https://github.com/tryton/bank.git',
        '--branch=3.4',
        'ado/src/bank'
    ),
    (
        'https://github.com/virtualthings/web_user.git',
        '--branch=3.4',
        'ado/src/web_user'
    ),
    (
        'https://github.com/C3S/collecting_society.git',
        '--branch=3.4',
        'ado/src/collecting_society'
    ),
    (
        'https://github.com/C3S/collecting_society.portal.git',
        '--branch=master',
        'ado/src/collecting_society.portal'
    ),
    (
        'https://github.com/C3S/collecting_society.portal.creative.git',
        '--branch=master',
        'ado/src/collecting_society.portal.creative',
    ),
    (
        'https://github.com/C3S/collecting_society.portal.imp.git',
        '--branch=master',
        'ado/src/collecting_society.portal.imp'
    ),
)

configfiles = (
    (
        'ado/etc/trytonpassfile.example',
        'ado/etc/trytonpassfile',
    ),
    (
        'portal.env.example',
        'portal.env'
    ),
    (
        'api.env.example',
        'api.env'
    ),
)
