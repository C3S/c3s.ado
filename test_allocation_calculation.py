# For copyright and license terms, see COPYRIGHT.rst (top level of repository)
# Repository: https://github.com/C3S/c3s.ado
import unittest
from decimal import Decimal


def allocate(creation, amount, precision=28, result=None):
    '''
    Allocates an amount to all involved artists of a creation.
    The tree of original creations is traversed and every node creation is
    allocated by the appropriate derivative types.

    Returns a list of tuples with artist as the first value and the share
    amount as the second position.
    '''
    amount = Decimal(amount)
    if result is None:
        result = [
            # (artist, hat_amount),
        ]

    # creator_contributions = [c for c in creation.contributions if c.type]
    compositions = [
        c.artist for c in creation.contributions if c.type == 'composition']
    texts = [
        c.artist for c in creation.contributions if c.type == 'text']
    performers = [
        c.artist for c in creation.contributions if c.type == 'performance']
    if performers and (texts or compositions):
        amount = amount / Decimal(2)

#    if creation.original_creations:
#        amount = amount / Decimal(2)

    # Composer calculation
    if compositions:
        composition_amount = amount
        if texts:
            composition_amount *= Decimal('.65')
        composition_amount /= Decimal(len(compositions))
        result.extend([(c, composition_amount) for c in compositions])

    # Writer calculation
    if texts:
        text_amount = amount
        if compositions:
            text_amount *= Decimal('.35')
        text_amount /= Decimal(len(texts))
        result.extend([(w, text_amount) for w in texts])

    # Performer calculation
    if performers:
        performer_amount = amount / Decimal(len(performers))
        result.extend([(p, performer_amount) for p in performers])

#    # Traverse Originators
#    for original in creation.original_creations:
#        if not original.derivative_type:
#            result = allocate(
#                creation=original.original_creation,
#                amount=amount / Decimal(len(creation.original_creations)),
#                result=result)

    if not creation.contributions:
        # Handle creations from unclaimed fingerprinting identification:
        # allocate complete amount to creation artist
        result.append((creation.artist, amount))

    return result


# Test stub classes
class CreationContribution(object):
    def __init__(self):
        self.artist = None
        self.type = None


class CreationOriginalDerivative(object):
    def __init__(self):
        self.original_creation = None
        self.derivative_type = ''


class Creation(object):
    def __init__(self):
        self.artist = None
        self.original_relations = []
        self.contributions = []


def total(allocation):
    return sum([x[1] for x in allocation]).quantize(Decimal('1'))


def parse(allocation):
    result = ''
    for line in allocation:
        result += '%s: %s\n' % line
    result = result.strip()
    return result


class AllocateTests(unittest.TestCase):
    def setUp(self):
        self.amount = Decimal('100')

    def test_10creation_artist(self):
        '1 creation, artist'
        creation = Creation()
        creation.artist = 'TOM'
        allocation = allocate(creation, self.amount)
        self.assertEqual(total(allocation), self.amount)
        self.assertEqual(
            parse(allocation),
            'TOM: 100')


    def test_20creation_artist_performance(self):
        '1 creation, artist,  1 performance'
        creation = Creation()
        creation.artist = 'TOM'
        contribution = CreationContribution()
        contribution.artist = 'Meik P'
        contribution.type = 'performance'
        creation.contributions = [contribution]

        allocation = allocate(creation, self.amount)
        self.assertEqual(total(allocation), self.amount)
        self.assertEqual(
            parse(allocation),
            'Meik P: 100')

    def test_30creation_artist_performance(self):
        '1 creation, 3 performance'
        creation = Creation()
        contribution1 = CreationContribution()
        contribution1.artist = 'meik P'
        contribution1.type = 'performance'
        contribution2 = CreationContribution()
        contribution2.artist = 'sarah P'
        contribution2.type = 'performance'
        contribution3 = CreationContribution()
        contribution3.artist = 'eva P'
        contribution3.type = 'performance'
        creation.contributions = [contribution1, contribution2, contribution3]
        allocation = allocate(creation, self.amount)
        self.assertEqual(total(allocation) - self.amount, Decimal(0))
        self.assertEqual(
            parse(allocation),
            'meik P: 33.33333333333333333333333333\n'
            'sarah P: 33.33333333333333333333333333\n'
            'eva P: 33.33333333333333333333333333')

    def test_40creation_artist_text(self):
        '1 creation, 1 text'
        creation = Creation()
        contribution = CreationContribution()
        contribution.artist = 'Frank W'
        contribution.type = 'text'
        creation.contributions = [contribution]
        allocation = allocate(creation, self.amount)
        self.assertEqual(total(allocation), self.amount)
        self.assertEqual(
            parse(allocation),
            'Frank W: 100')

    def test_50creation_artist_text(self):
        '1 creation 2 text'
        creation = Creation()
        creation.artist = 'TOM'

        contributions = CreationContribution()
        contributions.artist = 'Udo w'
        contributions.type = 'text'
        creation.contributions = [contributions]

        contributions = CreationContribution()
        contributions.artist = 'Christoph w'
        contributions.type = 'text'

        creation.contributions.append(contributions)
        allocation = allocate(creation, self.amount)
        self.assertEqual(total(allocation), self.amount)
        self.assertEqual(
            parse(allocation),
            'Udo w: 50\n'
            'Christoph w: 50')

    def Test_60creation_artist_composition(self):
        '1 creation 1 artist 2 composition'
        creation = Creation()
        creation.artist = 'TOM'

        contributions = CreationContribution()
        contributions.artist = 'Udo c'
        contributions.type = 'composition'
        creation.contributions = [contributions]
        contributions = CreationContribution()
        contributions.artist = 'Christoph c'
        contributions.type = 'composition'
        creation.contributions.append(contributions)
        allocation = allocate(creation, self.amount)
        self.assertEqual(total(allocation), self.amount)
        self.assertEqual(
            parse(allocation),
            'Meik P: 100')

    def test_70creation_artist_composition(self):
        '1 creation 1 artist 2 compositions 1 writer 2 performer'
        creation = Creation()
        creation.artist = 'TOM'
        contribution = CreationContribution()
        contribution.artist = 'Udo c'
        contribution.type = 'composition'
        creation.contributions = [contribution]
        contribution = CreationContribution()
        contribution.artist = 'Christoph c'
        contribution.type = 'composition'
        creation.contributions.append(contribution)
        contribution = CreationContribution()
        contribution.artist = 'Meik w'
        contribution.type = 'text'
        creation.contributions.append(contribution)
        contribution = CreationContribution()
        contribution.artist = 'sarah P'
        contribution.type = 'performance'
        creation.contributions.append(contribution)
        contribution = CreationContribution()
        contribution.artist = 'Frank P'
        contribution.type = 'performance'
        creation.contributions.append(contribution)
        allocation = allocate(creation, self.amount)
        self.assertEqual(total(allocation), self.amount)
        self.assertEqual(
            parse(allocation),
            'Udo c: 16.25\n'
            'Christoph c: 16.25\n'
            'Meik w: 17.50\n'
            'sarah P: 25\n'
            'Frank P: 25')


if __name__ == '__main__':
    unittest.main()

"""
#    Test creation with one composition and one text
contributions = CreationContribution()
contributions.artist = 'Udo c'
contributions.type = 'composition'
creation.contributions = [contributions]
contributions = CreationContribution()
contributions.artist = 'Christoph w'
contributions.type = 'text'
creation.contributions.append(contributions)
print(allocate(creation, amount))

#    Test creation with one composition, text, performer
contributions = CreationContribution()
contributions.artist = 'Udo c'
contributions.type = 'composition'
creation.contributions = [contributions]
contributions = CreationContribution()
contributions.artist = 'Christoph w'
contributions.type = 'text'
creation.contributions.append(contributions)
contributions = CreationContribution()
contributions.artist = 'Alex P'
creation.contributions.append(contributions)
print(allocate(creation, amount))

#    Test creation with two composition, text, performer
contributions = CreationContribution()
contributions.artist = 'Udo 1 c'
contributions.type = 'composition'
creation.contributions = [contributions]
contributions = CreationContribution()
contributions.artist = 'Udo 2 w'
contributions.type = 'text'
creation.contributions.append(contributions)
contributions = CreationContribution()
contributions.artist = 'Christoph 1 w'
contributions.type = 'text'
creation.contributions.append(contributions)
contributions = CreationContribution()
contributions.artist = 'Christoph 2 c'
contributions.type = 'composition'
creation.contributions.append(contributions)
contributions = CreationContribution()
contributions.artist = 'Alex 1 p'
creation.contributions.append(contributions)
contributions = CreationContribution()
contributions.artist = 'Alex 2 p'
creation.contributions.append(contributions)
print(allocate(creation, amount))

#
# Derived Works
#
#    Test artist only and .original_creations
amount = Decimal('100')
_creation = Creation()
_creation.artist = 'Featured Artist TOM original'
creation = Creation()
creation.artist = 'Featured Artist JERRY derived'
creation.original_creations.append(CreationOriginalDerivative())
creation.original_creations[0].original_creation = _creation
print(allocate(creation, amount))


#    Test creation with one original_creation with one Performer
contributions = CreationContribution()
contributions.artist = 'Meik P'
_creation.contributions.append(contributions)
print(allocate(creation, amount))

######
sys.exit()

#    Test creation with three Performer
contributions = CreationContribution()
contributions.artist = 'Sarah P'
creation.contributions.append(contributions)
contributions = CreationContribution()
contributions.artist = 'Eva P'
creation.contributions.append(contributions)
print(allocate(creation, amount))

#    Test creation with one text
contributions = CreationContribution()
contributions.artist = 'Frank w'
contributions.type = 'text'
creation.contributions = [contributions]
print(allocate(creation, amount))

#    Test creation with two texts
contributions = CreationContribution()
contributions.artist = 'Udo w'
contributions.type = 'text'
creation.contributions = [contributions]
contributions = CreationContribution()
contributions.artist = 'Christoph w'
contributions.type = 'text'

#    Test creation with two composition
contributions = CreationContribution()
contributions.artist = 'Udo c'
contributions.type = 'composition'
creation.contributions = [contributions]
contributions = CreationContribution()
contributions.artist = 'Christoph c'
contributions.type = 'composition'
creation.contributions.append(contributions)
print(allocate(creation, amount))

#    Test creation with one composition and one text
contributions = CreationContribution()
contributions.artist = 'Udo c'
contributions.type = 'composition'
creation.contributions = [contributions]
contributions = CreationContribution()
contributions.artist = 'Christoph w'
contributions.type = 'text'
creation.contributions.append(contributions)
print(allocate(creation, amount))

#    Test creation with one composition, text, performer
contributions = CreationContribution()
contributions.artist = 'Udo c'
contributions.type = 'composition'
creation.contributions = [contributions]
contributions = CreationContribution()
contributions.artist = 'Christoph w'
contributions.type = 'text'
creation.contributions.append(contributions)
contributions = CreationContribution()
contributions.artist = 'Alex P'
creation.contributions.append(contributions)
print(allocate(creation, amount))

#    Test creation with two composition, text, performer
contributions = CreationContribution()
contributions.artist = 'Udo 1 c'
contributions.type = 'composition'
creation.contributions = [contributions]
contributions = CreationContribution()
contributions.artist = 'Udo 2 w'
contributions.type = 'text'
creation.contributions.append(contributions)
contributions = CreationContribution()
contributions.artist = 'Christoph 1 w'
contributions.type = 'text'
creation.contributions.append(contributions)
contributions = CreationContribution()
contributions.artist = 'Christoph 2 c'
contributions.type = 'composition'
creation.contributions.append(contributions)
contributions = CreationContribution()
contributions.artist = 'Alex 1 p'
creation.contributions.append(contributions)
contributions = CreationContribution()
contributions.artist = 'Alex 2 p'
creation.contributions.append(contributions)
print(allocate(creation, amount))
res = 0
for line in allocate(creation, amount):
    res += line[1]
print('Sum %s' % res)
"""
