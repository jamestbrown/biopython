# Copyright (C) 2009 by Eric Talevich (eric.talevich@gmail.com)
# This code is part of the Biopython distribution and governed by its
# license. Please see the LICENSE file that should have been included
# as part of this package.

"""Unit tests for the PhyloXML and PhyloXMLIO modules.
"""

import os
import unittest
import zipfile
from itertools import izip, chain
from cStringIO import StringIO

from Bio.Phylo import PhyloXML as PX, PhyloXMLIO


# Example PhyloXML files
EX_APAF = 'PhyloXML/apaf.xml'
EX_BCL2 = 'PhyloXML/bcl_2.xml'
EX_MADE = 'PhyloXML/made_up.xml'
EX_PHYLO = 'PhyloXML/phyloxml_examples.xml'
EX_DOLLO = 'PhyloXML/o_tol_332_d_dollo.xml'
EX_MOLLUSCA = 'PhyloXML/ncbi_taxonomy_mollusca.xml.zip'
# Big files - not checked into git
EX_TOL = 'PhyloXML/tol_life_on_earth_1.xml.zip'
EX_METAZOA = 'PhyloXML/ncbi_taxonomy_metazoa.xml.zip'
EX_NCBI = 'PhyloXML/ncbi_taxonomy.xml.zip'


def unzip(fname):
    """Extract a single file from a Zip archive and return a handle to it."""
    assert zipfile.is_zipfile(fname)
    z = zipfile.ZipFile(fname)
    return StringIO(z.read(z.filelist[0].filename))


# ---------------------------------------------------------
# Utility tests

class UtilTests(unittest.TestCase):
    """Tests for PhyloXML utility functions."""
    def test_dump_tags(self):
        """Count and confirm the number of tags in each example XML file."""
        for source, count in izip(
                (EX_APAF, EX_BCL2, EX_PHYLO, unzip(EX_MOLLUSCA),
                    # unzip(EX_METAZOA), unzip(EX_NCBI),
                    ),
                (509, 1496, 289, 24311, 322367, 972830)):
            output = StringIO()
            PhyloXMLIO.dump_tags(source, output)
            output.seek(0)
            self.assertEquals(len(output.readlines()), count)


# ---------------------------------------------------------
# Parser tests

def _test_read_factory(source, count):
    """Generate a test method for read()ing the given source.

    The generated function reads an example file to produce a phyloXML object,
    then tests for existence of the root node, and counts the number of
    phylogenies under the root.
    """
    fname = os.path.basename(source)
    if zipfile.is_zipfile(source):
        source = unzip(source)
    def test_read(self):
        phx = PhyloXMLIO.read(source)
        self.assert_(phx)
        self.assertEquals(len(phx), count[0])
        self.assertEquals(len(phx.other), count[1])
    test_read.__doc__ = "Read %s to produce a phyloXML object." % fname
    return test_read


def _test_parse_factory(source, count):
    """Generate a test method for parse()ing the given source.

    The generated function extracts each phylogenetic tree using the parse()
    function and counts the total number of trees extracted.
    """
    fname = os.path.basename(source)
    if zipfile.is_zipfile(source):
        source = unzip(source)
    def test_parse(self):
        trees = PhyloXMLIO.parse(source)
        self.assertEquals(len(list(trees)), count)
    test_parse.__doc__ = "Parse the phylogenies in %s." % fname
    return test_parse


def _test_shape_factory(source, shapes):
    """Generate a test method for checking tree shapes.

    Counts the branches at each level of branching in a phylogenetic tree, 3
    clades deep.
    """
    fname = os.path.basename(source)
    if zipfile.is_zipfile(source):
        source = unzip(source)
    def test_shape(self):
        trees = PhyloXMLIO.parse(source)
        for tree, shape_expect in izip(trees, shapes):
            self.assertEquals(len(tree.clade), len(shape_expect))
            for clade, sub_expect in izip(tree.clade, shape_expect):
                self.assertEquals(len(clade), sub_expect[0])
                for subclade, len_expect in izip(clade, sub_expect[1]):
                    self.assertEquals(len(subclade), len_expect)
    test_shape.__doc__ = "Check the branching structure of %s." % fname
    return test_shape


class ParseTests(unittest.TestCase):
    """Tests for proper parsing of example phyloXML files."""

    test_read_apaf = _test_read_factory(EX_APAF, (1, 0))
    test_read_bcl2 = _test_read_factory(EX_BCL2, (1, 0))
    test_read_made = _test_read_factory(EX_MADE, (6, 0))
    test_read_phylo = _test_read_factory(EX_PHYLO, (13, 1))
    test_read_dollo = _test_read_factory(EX_DOLLO, (1, 0))
    test_read_mollusca = _test_read_factory(EX_MOLLUSCA, (1, 0))

    test_parse_apaf = _test_parse_factory(EX_APAF, 1)
    test_parse_bcl2 = _test_parse_factory(EX_BCL2, 1)
    test_parse_made = _test_parse_factory(EX_MADE, 6)
    test_parse_phylo = _test_parse_factory(EX_PHYLO, 13)
    test_parse_dollo = _test_parse_factory(EX_DOLLO, 1)
    test_parse_mollusca = _test_parse_factory(EX_MOLLUSCA, 1)

    test_shape_apaf = _test_shape_factory(EX_APAF,
            # lvl-2 clades, sub-clade counts, lvl-3 clades
                ( ( (2, (2, 2)),
                    (2, (2, 2)),
                  ),
                ),
            )
    test_shape_bcl2 = _test_shape_factory(EX_BCL2,
                ( ( (2, (2, 2)),
                    (2, (2, 2)),
                  ),
                ),
            )
    test_shape_phylo = _test_shape_factory(EX_PHYLO,
                ( ( (2, (0, 0)),
                    (0, ()),
                  ),
                  ( (2, (0, 0)),
                    (0, ()),
                  ),
                  ( (2, (0, 0)),
                    (0, ()),
                  ),
                  ( (2, (0, 0)),
                    (0, ()),
                  ),
                  ( (2, (0, 0)),
                    (0, ()),
                  ),
                  ( (2, (0, 0)),
                    (0, ()),
                  ),
                  ( (2, (0, 0)),
                    (0, ()),
                  ),
                  ( (2, (0, 0)),
                    (0, ()),
                  ),
                  ( (2, (0, 0)),
                    (0, ()),
                  ),
                  ( (0, ()),
                    (2, (0, 0)),
                  ),
                  ( (3, (0, 0, 0)),
                    (0, ()),
                  ),
                  ( (2, (0, 0)),
                    (0, ()),
                  ),
                  ( (2, (0, 0)),
                    (0, ()),
                  ),
                ),
            )
    test_shape_dollo = _test_shape_factory(EX_DOLLO,
                ( ( (2, (2, 2)),
                    (2, (2, 2)),
                  ),
                ),
            )
    test_shape_zip = _test_shape_factory(EX_MOLLUSCA,
                ( ( (3, (5, 1, 4)),
                    (5, (6, 2, 2, 2, 1)),
                    (2, (1, 1)),
                    (1, (2,)),
                    (2, (4, 4)),
                    (2, (2, 2)),
                    (1, (1,)),
                  ),
                ),
            )


class TreeTests(unittest.TestCase):
    """Tests for instantiation and attributes of each complex type."""
    # ENH: also test check_str() regexps wherever they're used
    def test_Phyloxml(self):
        """Instantiation of Phyloxml objects."""
        phx = PhyloXMLIO.read(EX_PHYLO)
        self.assert_(isinstance(phx, PX.Phyloxml))
        for tree in phx:
            self.assert_(isinstance(tree, PX.Phylogeny))
        for otr in phx.other:
            self.assert_(isinstance(otr, PX.Other))

    def test_Other(self):
        """Instantiation of Other objects."""
        phx = PhyloXMLIO.read(EX_PHYLO)
        otr = phx.other[0]
        self.assert_(isinstance(otr, PX.Other))
        self.assertEquals(otr.tag, 'alignment')
        self.assertEquals(otr.namespace, 'http://example.org/align')
        self.assertEquals(len(otr.children), 3)
        for child, name, value in izip(otr, ('A', 'B', 'C'), (
            'acgtcgcggcccgtggaagtcctctcct', 'aggtcgcggcctgtggaagtcctctcct',
            'taaatcgc--cccgtgg-agtccc-cct')):
            self.assertEquals(child.tag, 'seq')
            self.assertEquals(child.attributes['name'], name)
            self.assertEquals(child.value, value)

    def test_Phylogeny(self):
        """Instantiation of Phylogeny objects."""
        trees = list(PhyloXMLIO.parse(EX_PHYLO))
        # Monitor lizards
        self.assertEquals(trees[9].name, 'monitor lizards')
        self.assertEquals(trees[9].description,
                'a pylogeny of some monitor lizards')
        self.assertEquals(trees[9].rooted, True)
        # Network (unrooted)
        tree6 = trees[6]
        self.assertEquals(trees[6].name,
                'network, node B is connected to TWO nodes: AB and C')
        self.assertEquals(trees[6].rooted, False)

    def test_Clade(self):
        """Instantiation of Clade objects."""
        tree = list(PhyloXMLIO.parse(EX_PHYLO))[6]
        clade_ab, clade_c = tree.clade.clades
        clade_a, clade_b = clade_ab.clades
        for clade, id_source, name, blen in izip(
                (clade_ab, clade_a, clade_b, clade_c),
                ('ab', 'a', 'b', 'c'),
                ('AB', 'A', 'B', 'C'),
                (0.06, 0.102, 0.23, 0.4)):
            self.assert_(isinstance(clade, PX.Clade))
            self.assertEqual(clade.id_source, id_source)
            self.assertEqual(clade.name, name)
            self.assertAlmostEqual(clade.branch_length, blen)

    def test_Annotation(self):
        """Instantiation of Annotation objects."""
        tree = list(PhyloXMLIO.parse(EX_PHYLO))[3]
        ann = tree.clade[1].sequences[0].annotations[0]
        self.assert_(isinstance(ann, PX.Annotation))
        self.assertEqual(ann.desc, 'alcohol dehydrogenase')
        self.assertAlmostEqual(ann.confidence.value, 0.67)
        self.assertEqual(ann.confidence.type, 'probability')

    def test_BinaryCharacters(self):
        """Instantiation of BinaryCharacters objects."""
        tree = PhyloXMLIO.parse(EX_DOLLO).next()
        bchars = tree.clade[0,0].binary_characters
        self.assert_(isinstance(bchars, PX.BinaryCharacters))
        self.assertEqual(bchars.type, 'parsimony inferred')
        for name, count, value in (
                ('gained',  2, ['Cofilin_ADF', 'Gelsolin']),
                ('lost',    0, []),
                ('present', 2, ['Cofilin_ADF', 'Gelsolin']),
                ('absent',  None, []),
                ):
            self.assertEqual(getattr(bchars, name+'_count'), count)
            self.assertEqual(getattr(bchars, name), value)

    # BranchColor -- no example

    def test_CladeRelation(self):
        """Instantiation of CladeRelation objects."""
        tree = list(PhyloXMLIO.parse(EX_PHYLO))[6]
        crel = tree.clade_relations[0]
        self.assert_(isinstance(crel, PX.CladeRelation))
        self.assertEqual(crel.id_ref_0, 'b')
        self.assertEqual(crel.id_ref_1, 'c')
        self.assertEqual(crel.type, 'network_connection')

    def test_Confidence(self):
        """Instantiation of Confidence objects."""
        tree = PhyloXMLIO.parse(EX_MADE).next()
        self.assertEqual(tree.name, 'testing confidence')
        for conf, type, val in izip(tree.confidences,
                ('bootstrap', 'probability'),
                (89.0, 0.71)):
            self.assert_(isinstance(conf, PX.Confidence))
            self.assertEqual(conf.type, type)
            self.assertAlmostEqual(conf.value, val)
        self.assertEqual(tree.clade.name, 'b')
        self.assertAlmostEqual(tree.clade.width, 0.2)
        for conf, val in izip(tree.clade[0].confidences,
                (0.9, 0.71)):
            self.assert_(isinstance(conf, PX.Confidence))
            self.assertEqual(conf.type, 'probability')
            self.assertAlmostEqual(conf.value, val)

    def test_Date(self):
        """Instantiation of Date objects."""
        tree = list(PhyloXMLIO.parse(EX_PHYLO))[11]
        silurian = tree.clade[0,0].date
        devonian = tree.clade[0,1].date
        ediacaran = tree.clade[1].date
        for date, desc, val in izip(
                (silurian, devonian, ediacaran),
                # (10, 20, 30), # range is deprecated
                ('Silurian', 'Devonian', 'Ediacaran'),
                (425, 320, 600)):
            self.assert_(isinstance(date, PX.Date))
            self.assertEqual(date.unit, 'mya')
            # self.assertAlmostEqual(date.range, rang)
            self.assertEqual(date.desc, desc)
            self.assertAlmostEqual(date.value, val)

    def test_Distribution(self):
        """Instantiation of Distribution objects.

        Also checks Point type and safe Unicode handling (?).
        """
        tree = list(PhyloXMLIO.parse(EX_PHYLO))[10]
        hirschweg = tree.clade[0,0].distributions[0]
        nagoya = tree.clade[0,1].distributions[0]
        eth_zurich = tree.clade[0,2].distributions[0]
        san_diego = tree.clade[1].distributions[0]
        for dist, desc, lat, long, alt in izip(
                (hirschweg, nagoya, eth_zurich, san_diego),
                ('Hirschweg, Winterthur, Switzerland',
                    'Nagoya, Aichi, Japan',
                    u'ETH Z\xfcrich',
                    'San Diego'),
                (47.481277, 35.155904, 47.376334, 32.880933),
                (8.769303, 136.915863, 8.548108, -117.217543),
                (472, 10, 452, 104)):
            self.assert_(isinstance(dist, PX.Distribution))
            self.assertEqual(dist.desc, desc)
            point = dist.points[0]
            self.assert_(isinstance(point, PX.Point))
            self.assertEqual(point.geodetic_datum, 'WGS84')
            self.assertEqual(point.lat, lat)
            self.assertEqual(point.long, long)
            self.assertEqual(point.alt, alt)

    def test_DomainArchitecture(self):
        """Instantiation of DomainArchitecture objects.

        Also checks ProteinDomain type.
        """
        tree = PhyloXMLIO.parse(EX_APAF).next()
        clade = tree.clade[0,0,0,0,0,0,0,0,0,0]
        darch = clade.sequences[0].domain_architecture
        self.assert_(isinstance(darch, PX.DomainArchitecture))
        self.assertEqual(darch.length, 1249)
        for domain, start, end, conf, value in izip(darch.domains,
                (6, 109, 605, 647, 689, 733, 872, 993, 1075, 1117, 1168),
                (90, 414, 643, 685, 729, 771, 910, 1031, 1113, 1155, 1204),
                (7.0e-26, 7.2e-117, 2.4e-6, 1.1e-12, 2.4e-7, 4.7e-14, 2.5e-8,
                    4.6e-6, 6.3e-7, 1.4e-7, 0.3),
                ('CARD', 'NB-ARC', 'WD40', 'WD40', 'WD40', 'WD40', 'WD40',
                    'WD40', 'WD40', 'WD40', 'WD40')):
            self.assert_(isinstance(domain, PX.ProteinDomain))
            self.assertEqual(domain.start + 1, start)
            self.assertEqual(domain.end, end)
            self.assertAlmostEqual(domain.confidence, conf)
            self.assertEqual(domain.value, value)

    def test_Events(self):
        """Instantiation of Events objects."""
        tree = list(PhyloXMLIO.parse(EX_PHYLO))[4]
        event_s = tree.clade.events
        self.assert_(isinstance(event_s, PX.Events))
        self.assertEqual(event_s.speciations, 1)
        event_d = tree.clade[0].events
        self.assert_(isinstance(event_d, PX.Events))
        self.assertEqual(event_d.duplications, 1)

    def test_Polygon(self):
        """Instantiation of Polygon objects."""
        tree = PhyloXMLIO.read(EX_MADE).phylogenies[1]
        self.assertEqual(tree.name, 'testing polygon')
        dist = tree.clade[0].distributions[0]
        for poly in dist.polygons:
            self.assert_(isinstance(poly, PX.Polygon))
            self.assertEqual(len(poly.points), 3)
        self.assertEqual(dist.polygons[0].points[0].alt_unit, 'm')
        for point, lat, long, alt in izip(
                chain(dist.polygons[0].points, dist.polygons[1].points),
                (47.481277, 35.155904, 47.376334, 40.481277, 25.155904,
                    47.376334),
                (8.769303, 136.915863, 8.548108, 8.769303, 136.915863,
                    7.548108),
                (472, 10, 452, 42, 10, 452),
                ):
            self.assert_(isinstance(point, PX.Point))
            self.assertEqual(point.geodetic_datum, 'WGS84')
            self.assertEqual(point.lat, lat)
            self.assertEqual(point.long, long)
            self.assertEqual(point.alt, alt)

    def test_Property(self):
        """Instantiation of Property objects."""
        tree = list(PhyloXMLIO.parse(EX_PHYLO))[8]
        for prop, id_ref, value in izip(
                tree.properties,
                ('id_a', 'id_b', 'id_c'),
                ('1200', '2300', '200')):
            self.assert_(isinstance(prop, PX.Property))
            self.assertEqual(prop.id_ref, id_ref)
            self.assertEqual(prop.datatype, "xsd:integer")
            self.assertEqual(prop.ref, "NOAA:depth")
            self.assertEqual(prop.applies_to, "node")
            self.assertEqual(prop.unit, "METRIC:m" )
            self.assertEqual(prop.value, value)

    def test_Reference(self):
        """Instantiation of Reference objects."""
        tree = PhyloXMLIO.parse(EX_DOLLO).next()
        reference = tree.clade[0,0,0,0,0,0].references[0]
        self.assert_(isinstance(reference, PX.Reference))
        self.assertEqual(reference.doi, '10.1038/nature06614')
        self.assertEqual(reference.desc, None)

    def test_Sequence(self):
        """Instantiation of Sequence objects.

        Also checks Accession and Annotation types.
        """
        trees = list(PhyloXMLIO.parse(EX_PHYLO))
        # Simple element with id_source
        seq0 = trees[4].clade[1].sequences[0]
        self.assert_(isinstance(seq0, PX.Sequence))
        self.assertEqual(seq0.id_source, 'z')
        self.assertEqual(seq0.symbol, 'ADHX')
        self.assertEqual(seq0.accession.source, 'ncbi')
        self.assertEqual(seq0.accession.value, 'Q17335')
        self.assertEqual(seq0.name, 'alcohol dehydrogenase')
        self.assertEqual(seq0.annotations[0].ref, 'InterPro:IPR002085')
        # More complete elements
        seq1 = trees[5].clade[0,0].sequences[0]
        seq2 = trees[5].clade[0,1].sequences[0]
        seq3 = trees[5].clade[1].sequences[0]
        for seq, sym, acc, name, mol_seq, ann_refs in izip(
                (seq1, seq2, seq3),
                ('ADHX', 'RT4I1', 'ADHB'),
                ('P81431', 'Q54II4', 'Q04945'),
                ('Alcohol dehydrogenase class-3',
                 'Reticulon-4-interacting protein 1 homolog, ' \
                         'mitochondrial precursor',
                 'NADH-dependent butanol dehydrogenase B'),
                ('TDATGKPIKCMAAIAWEAKKPLSIEEVEVAPPKSGEVRIKILHSGVCHTD',
                 'MKGILLNGYGESLDLLEYKTDLPVPKPIKSQVLIKIHSTSINPLDNVMRK',
                 'MVDFEYSIPTRIFFGKDKINVLGRELKKYGSKVLIVYGGGSIKRNGIYDK'),
                (("EC:1.1.1.1", "GO:0004022"),
                 ("GO:0008270", "GO:0016491"),
                 ("GO:0046872", "KEGG:Tetrachloroethene degradation")),
                ):
            self.assert_(isinstance(seq, PX.Sequence))
            self.assertEqual(seq.symbol, sym)
            self.assertEqual(seq.accession.source, 'UniProtKB')
            self.assertEqual(seq.accession.value, acc)
            self.assertEqual(seq.name, name)
            self.assertEqual(seq.mol_seq.value, mol_seq)
            self.assertEqual(seq.annotations[0].ref, ann_refs[0])
            self.assertEqual(seq.annotations[1].ref, ann_refs[1])

    def test_SequenceRelation(self):
        """Instantiation of SequenceRelation objects."""
        tree = list(PhyloXMLIO.parse(EX_PHYLO))[4]
        for seqrel, id_ref_0, id_ref_1, type in izip(
                tree.sequence_relations,
                ('x', 'x', 'y'), ('y', 'z', 'z'),
                ('paralogy', 'orthology', 'orthology')):
            self.assert_(isinstance(seqrel, PX.SequenceRelation))
            self.assertEqual(seqrel.id_ref_0, id_ref_0)
            self.assertEqual(seqrel.id_ref_1, id_ref_1)
            self.assertEqual(seqrel.type, type)

    def test_Taxonomy(self):
        """Instantiation of Taxonomy objects.

        Also checks Id type.
        """
        trees = list(PhyloXMLIO.parse(EX_PHYLO))
        # Octopus
        tax5 = trees[5].clade[0,0].taxonomies[0]
        self.assert_(isinstance(tax5, PX.Taxonomy))
        self.assertEqual(tax5.id.value, '6645')
        self.assertEqual(tax5.id.provider, 'NCBI')
        self.assertEqual(tax5.code, 'OCTVU')
        self.assertEqual(tax5.scientific_name, 'Octopus vulgaris')
        # Nile monitor
        tax9 = trees[9].clade[0].taxonomies[0]
        self.assert_(isinstance(tax9, PX.Taxonomy))
        self.assertEqual(tax9.id.value, '62046')
        self.assertEqual(tax9.id.provider, 'NCBI')
        self.assertEqual(tax9.scientific_name, 'Varanus niloticus')
        self.assertEqual(tax9.common_names[0], 'Nile monitor')
        self.assertEqual(tax9.rank, 'species')

    def test_Uri(self):
        """Instantiation of Uri objects."""
        tree = list(PhyloXMLIO.parse(EX_PHYLO))[9]
        uri = tree.clade.taxonomies[0].uri
        self.assert_(isinstance(uri, PX.Uri))
        self.assertEqual(uri.desc, 'EMBL REPTILE DATABASE')
        self.assertEqual(uri.value,
                'http://www.embl-heidelberg.de/~uetz/families/Varanidae.html')


# ---------------------------------------------------------
# Serialization tests

class WriterTests(unittest.TestCase):
    """Tests for serialization of objects to phyloXML format."""
    def _stash_rewrite_and_call(self, fname, test_cases):
        """Safely run a series of tests on a parsed and rewritten file.

        Specifically: Parse a file, rename the source file to a backup, rewrite
        the file from the parsed object, check the rewritten file with the
        given series of test functions, then restore the original by renaming
        the backup copy.

        Python 2.4 support: This would make more sense as a context manager
        that simply handles renaming and finally restoring the original.
        """
        phx = PhyloXMLIO.read(fname)
        os.rename(fname, fname + '~')
        try:
            PhyloXMLIO.write(phx, fname)
            for cls, tests in test_cases:
                inst = cls('setUp')
                for test in tests:
                    getattr(inst, test)()
        finally:
            os.rename(fname + '~', fname)

    def test_apaf(self):
        """Round-trip parsing and serialization of apaf.xml."""
        self._stash_rewrite_and_call(EX_APAF, (
            (ParseTests, [
                'test_read_apaf', 'test_parse_apaf', 'test_shape_apaf']),
            (TreeTests, ['test_DomainArchitecture']),
            ))

    def test_bcl2(self):
        """Round-trip parsing and serialization of bcl_2.xml."""
        self._stash_rewrite_and_call(EX_BCL2, (
            (ParseTests, [
                'test_read_bcl2', 'test_parse_bcl2', 'test_shape_bcl2']),
            (TreeTests, ['test_Confidence']),
            ))

    def test_made(self):
        """Round-trip parsing and serialization of made_up.xml."""
        self._stash_rewrite_and_call(EX_MADE, (
            (ParseTests, ['test_read_made', 'test_parse_made']),
            (TreeTests, ['test_Confidence', 'test_Polygon']),
            ))

    def test_phylo(self):
        """Round-trip parsing and serialization of phyloxml_examples.xml."""
        self._stash_rewrite_and_call(EX_PHYLO, (
            (ParseTests, [
                'test_read_phylo', 'test_parse_phylo', 'test_shape_phylo']),
            (TreeTests, [
                'test_Phyloxml',   'test_Other',
                'test_Phylogeny',  'test_Clade',
                'test_Annotation', 'test_CladeRelation',
                'test_Date',       'test_Distribution',
                'test_Events',     'test_Property',
                'test_Sequence',   'test_SequenceRelation',
                'test_Taxonomy',   'test_Uri',
                ]),
            ))

    def test_dollo(self):
        """Round-trip parsing and serialization of o_tol_332_d_dollo.xml."""
        self._stash_rewrite_and_call(EX_DOLLO, (
            (ParseTests, ['test_read_dollo', 'test_parse_dollo']),
            (TreeTests, ['test_BinaryCharacters']),
            ))


# ---------------------------------------------------------
# Method tests

class MethodTests(unittest.TestCase):
    """Tests for methods on specific classes/objects."""
    def setUp(self):
        self.phyloxml = PhyloXMLIO.read(EX_PHYLO)

    # Type conversions

    def test_clade_to_phylogeny(self):
        """Convert a Clade object to a new Phylogeny."""
        clade = self.phyloxml.phylogenies[0].clade[0]
        tree = clade.to_phylogeny(rooted=True)
        self.assert_(isinstance(tree, PX.Phylogeny))

    def test_phylogeny_to_phyloxml(self):
        """Convert a Phylogeny object to a new Phyloxml."""
        tree = self.phyloxml.phylogenies[0]
        doc = tree.to_phyloxml()
        self.assert_(isinstance(doc, PX.Phyloxml))

    def test_sequence_conversion(self):
        pseq = PX.Sequence(
            type='protein',
            # id_ref=None,
            # id_source=None,
            symbol='ADHX',
            accession=PX.Accession('P81431', source='UniProtKB'),
            name='Alcohol dehydrogenase class-3',
            # location=None,
            mol_seq=PX.MolSeq(
                'TDATGKPIKCMAAIAWEAKKPLSIEEVEVAPPKSGEVRIKILHSGVCHTD'),
            uri=None,
            annotations=[PX.Annotation(ref='EC:1.1.1.1'),
                         PX.Annotation(ref='GO:0004022')],
            domain_architecture=PX.DomainArchitecture(
                length=50,
                domains=[PX.ProteinDomain(*args) for args in (
                    # value,   start,   end,    confidence
                    ('FOO',     0,      5,      7.0e-26),
                    ('BAR',     8,      13,     7.2e-117),
                    ('A-OK',    21,     34,     2.4e-06),
                    ('WD40',    40,     50,     0.3))],
                ))
        srec = pseq.to_seqrecord()
        # TODO: check seqrec-specific traits (see args)
        #   Seq(letters, alphabet), id, name, description, features
        pseq2 = PX.Sequence.from_seqrecord(srec)
        # TODO: check the round-tripped attributes again


    def test_get_alignment(self):
        # TODO: load a Phylogeny w/ aligned Sequences, call, check attrs
        pass

    # Syntax sugar

    def test_clade_getitem(self):
        """Clade.__getitem__: get sub-clades by extended indexing."""
        tree = self.phyloxml.phylogenies[3]
        self.assertEqual(tree.clade[0,0], tree.clade.clades[0].clades[0])
        self.assertEqual(tree.clade[0,1], tree.clade.clades[0].clades[1])
        self.assertEqual(tree.clade[1], tree.clade.clades[1])
        self.assertEqual(len(tree.clade[:]), len(tree.clade.clades))
        self.assertEqual(len(tree.clade[0,:]),
                         len(tree.clade.clades[0].clades))

    def test_phyloxml_getitem(self):
        """Phyloxml.__getitem__: get phylogenies by name or index."""
        self.assert_(self.phyloxml.phylogenies[9] is self.phyloxml[9])
        self.assert_(self.phyloxml['monitor lizards'] is self.phyloxml[9])
        self.assertEqual(len(self.phyloxml[:]), len(self.phyloxml))

    def test_events(self):
        """Events: Mapping-type behavior."""
        evts = self.phyloxml.phylogenies[4].clade.events
        # Container behavior: __len__, __contains__
        self.assertEquals(len(evts), 1)
        self.assertEqual('speciations' in evts, True)
        self.assertEqual('duplications' in evts, False)
        # Attribute access: __get/set/delitem__
        self.assertEqual(evts['speciations'], 1)
        self.assertRaises(KeyError, lambda k: evts[k], 'duplications')
        evts['duplications'] = 3
        self.assertEqual(evts.duplications, 3)
        self.assertEqual(len(evts), 2)
        del evts['speciations']
        self.assertEqual(evts.speciations, None)
        self.assertEquals(len(evts), 1)
        # Iteration: __iter__, keys, values, items
        self.assertEqual(list(iter(evts)), ['duplications'])
        self.assertEqual(evts.keys(), ['duplications'])
        self.assertEqual(evts.values(), [3])
        self.assertEqual(evts.items(), [('duplications', 3)])

    def test_singlular(self):
        """Clade, Phylogeny: Singular properties for plural attributes."""
        conf = PX.Confidence(0.9, 'bootstrap')
        taxo = PX.Taxonomy(rank='genus')
        # Clade.taxonomy, Clade.confidence
        clade = PX.Clade(confidences=[conf], taxonomies=[taxo])
        self.assertEqual(clade.confidence.type, 'bootstrap')
        self.assertEqual(clade.taxonomy.rank, 'genus')
        # raise if len > 1
        clade.confidences.append(conf)
        self.assertRaises(ValueError, getattr, clade, 'confidence')
        clade.taxonomies.append(taxo)
        self.assertRaises(ValueError, getattr, clade, 'taxonomy')
        # raise if []
        clade.confidences = []
        self.assertRaises(AttributeError, getattr, clade, 'confidence')
        clade.taxonomies = []
        self.assertRaises(AttributeError, getattr, clade, 'taxonomy')
        # Phylogeny.confidence
        tree = PX.Phylogeny(True, confidences=[conf])
        self.assertEqual(tree.confidence.type, 'bootstrap')
        tree.confidences.append(conf)
        self.assertRaises(ValueError, getattr, tree, 'confidence')
        tree.confidences = []
        self.assertRaises(AttributeError, getattr, tree, 'confidence')

    # Other methods

    def test_color_hex(self):
        """BranchColor: to_hex() method."""
        black = PX.BranchColor(0, 0, 0)
        self.assertEqual(black.to_hex(), '#000000')
        white = PX.BranchColor(255, 255, 255)
        self.assertEqual(white.to_hex(), '#ffffff')
        green = PX.BranchColor(14, 192, 113)
        self.assertEqual(green.to_hex(), '#0ec071')

# ---------------------------------------------------------

if __name__ == '__main__':
    runner = unittest.TextTestRunner(verbosity=2)
    unittest.main(testRunner=runner)
