# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import contextlib
import os.path
import unittest

from mypy import api


@contextlib.contextmanager
def set_env(new_env_dict):
    """Temporarily set the process environment variables"""
    old_environ = dict(os.environ)
    os.environ.update(new_env_dict)
    try:
        yield
    finally:
        os.environ.clear()
        os.environ.update(old_environ)


class MypyTestCase(unittest.TestCase):
    mypy_config = os.path.dirname(__file__) + "/mypy_test.ini"

    def run_mypy(self, code):
        stdout, stderr, retcode = api.run(
            ["--config-file", self.mypy_config, "-c", code]
        )
        return stdout


SIMPLE_OVO = """
from oslo_versionedobjects import base as ovo_base
from oslo_versionedobjects import fields

@ovo_base.VersionedObjectRegistry.objectify
class MyOvo(ovo_base.VersionedObject):
    fields = {
        'id': fields.IntegerField(),
        'name': fields.StringField(),
        'temperature': fields.FloatField(),
        'list_of_ints': fields.ListOfIntegersField(),
    }

    def foo(self) -> None:
        return None

myobj: MyOvo
"""


class OvoMypyFieldTests(MypyTestCase):
    def test_basic_field_types_are_inferred(self):
        self.assertIn(
            "Revealed type is 'builtins.int",
            self.run_mypy(SIMPLE_OVO + "reveal_type(myobj.id)"),
        )

        self.assertIn(
            "Revealed type is 'builtins.str",
            self.run_mypy(SIMPLE_OVO + "reveal_type(myobj.name)"),
        )

        self.assertIn(
            "Revealed type is 'builtins.float",
            self.run_mypy(SIMPLE_OVO + "reveal_type(myobj.temperature)"),
        )

        self.assertIn(
            "Revealed type is 'builtins.list[builtins.int]",
            self.run_mypy(SIMPLE_OVO + "reveal_type(myobj.list_of_ints)"),
        )

        self.assertIn(
            "Incompatible types in assignment "
            '(expression has type "str", variable has type "int"',
            self.run_mypy(SIMPLE_OVO + "myobj.id = 'bob'"),
        )

    def test_non_existent_field_usage_is_caught(self):
        self.assertIn(
            '"MyOvo" has no attribute "nonexistent"',
            self.run_mypy(SIMPLE_OVO + "myobj.nonexistent"),
        )
        self.assertIn(
            '"MyOvo" has no attribute "nonexistent"',
            self.run_mypy(SIMPLE_OVO + "myobj.nonexistent = 12"),
        )


INDIRECT_BASE = """
from oslo_versionedobjects import base as ovo_base
from oslo_versionedobjects import fields

class MyBase(ovo_base.VersionedObject):
    pass

class MyOvo(MyBase):
    fields = {
        'id': fields.IntegerField(),
    }

    def foo(self) -> None:
        return None

myobj: MyOvo
"""


INDIRECT_DECORATOR = """
from oslo_versionedobjects import base as ovo_base
from oslo_versionedobjects import fields

my_decorator = ovo_base.VersionedObjectRegistry.objectify

class MyBase(ovo_base.VersionedObject):
    pass

@my_decorator
class MyOvo(MyBase):
    fields = {
        'id': fields.IntegerField(),
    }

    def foo(self) -> None:
        return None

myobj: MyOvo
"""


class OvoMypyConfigTests(MypyTestCase):
    def test_base_class_can_be_defined_in_the_env(self):
        self.assertNotIn(
            "Revealed type is 'builtins.int",
            self.run_mypy(INDIRECT_BASE + "reveal_type(myobj.id)"),
        )

        with set_env({"OVO_MYPY_BASE_CLASSES": "MyBase"}):
            self.assertIn(
                "Revealed type is 'builtins.int",
                self.run_mypy(INDIRECT_BASE + "reveal_type(myobj.id)"),
            )

    def test_decorator_class_can_be_defined_in_the_env(self):
        self.assertNotIn(
            "Revealed type is 'builtins.int",
            self.run_mypy(INDIRECT_DECORATOR + "reveal_type(myobj.id)"),
        )

        with set_env({"OVO_MYPY_DECORATOR_CLASSES": "my_decorator"}):
            self.assertIn(
                "Revealed type is 'builtins.int",
                self.run_mypy(INDIRECT_DECORATOR + "reveal_type(myobj.id)"),
            )


INHERITED_FIELDS = """
from oslo_versionedobjects import base as ovo_base
from oslo_versionedobjects import fields

@ovo_base.VersionedObjectRegistry.objectify
class IdBase(ovo_base.VersionedObject):
    fields = {
        'id': fields.IntegerField(),
    }

@ovo_base.VersionedObjectRegistry.objectify
class MyOvo(IdBase):
    fields = {
        'name': fields.StringField(),
    }

    def foo(self) -> None:
        return None

myobj: MyOvo
"""


class OvoInheritanceTests(MypyTestCase):
    def test_inherited_fields_are_known(self):
        self.assertIn(
            "Revealed type is 'builtins.int",
            self.run_mypy(INHERITED_FIELDS + "reveal_type(myobj.id)"),
        )

        self.assertIn(
            "Revealed type is 'builtins.str",
            self.run_mypy(INHERITED_FIELDS + "reveal_type(myobj.name)"),
        )
