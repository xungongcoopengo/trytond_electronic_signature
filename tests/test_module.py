# This file is part of Coog. The COPYRIGHT file at the top level of
# this repository contains the full copyright notices and license terms.
import datetime
import os

import unittest

import trytond.tests.test_tryton
from trytond.tests.test_tryton import ModuleTestCase, with_transaction

from trytond.modules.currency.tests import create_currency

from trytond.pool import Pool


class ElectronicSignatureTestCase(ModuleTestCase):
    'Module Test Case'
    module = 'electronic_signature'

    @with_transaction()
    def test_universign_with_id_documents(self):
        'Test Universign'
        pool = Pool()
        Party = pool.get('party.party')
        subscriber = Party()
        subscriber.name = 'Bertier'
        subscriber.first_name = 'Corinne'
        subscriber.is_person = True
        subscriber.gender = 'male'
        subscriber.birth_date = datetime.date(1965, 12, 6)
        subscriber.phone = '0612345678'
        subscriber.mobile = '0612345678'
        subscriber.email = 'corinne.bertier@coopengo.com'
        subscriber.all_addresses = ['home, sweet home']
        subscriber.save()

        Company = pool.get('company.company')
        company = Company()
        company.party = subscriber
        company.currency = create_currency('EUR')
        company.save()

        SignatureCredential = pool.get('document.signature.credential')
        signature_credential = SignatureCredential()
        signature_credential.company = company
        signature_credential.provider = ''
        signature_credential.provider_url = 'https://sign.test.cryptolog.com/sign/rpc'
        signature_credential.username = 'test.coopengo@universign.com'
        signature_credential.password = 'EGC0S50W'
        signature_credential.save()

        Signature = pool.get('document.signature')
        signature = Signature()
        signature.provider_credential = signature_credential
        signature.save()

        id_type = 'id_card_fr'
        id_docs = []
        id_docs_path = ('CNI-FR-TEST-RECTO.jpg',
            'CNI-FR-TEST-VERSO.jpg')

        module_file = __file__
        module_tests_folder = os.path.dirname(module_file)

        file_path = os.path.join(module_tests_folder, 'id_documents/')

        for id_doc_path in id_docs_path:
            with open(os.path.join(file_path, id_doc_path), 'rb') as id_doc:
                id_docs.append(id_doc.read())

        res = signature.validate_electronic_identity(subscriber, id_docs, id_type)

        self.assertTrue(res)


def suite():
    suite = trytond.tests.test_tryton.suite()
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(ElectronicSignatureTestCase))
    return suite
