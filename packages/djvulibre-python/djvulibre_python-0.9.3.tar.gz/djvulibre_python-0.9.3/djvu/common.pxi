# Copyright © 2008-2018 Jakub Wilk <jwilk@jwilk.net>
# Copyright © 2022-2024 FriedrichFroebel
#
# This file is part of djvulibre-python.
#
# djvulibre-python is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License version 2 as published by
# the Free Software Foundation.
#
# djvulibre-python is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
# or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for
# more details.

include 'config.pxi'

# C library:

from libc.stdlib cimport free  # noqa: F401
from libc.string cimport strlen  # noqa: E402

# Python memory handling:

from cpython.mem cimport PyMem_Malloc as py_malloc  # noqa: F401
from cpython.mem cimport PyMem_Free as py_free  # noqa: F401

# Python numbers:

from cpython cimport PyLong_Check

cdef int is_int(object o):
    return PyLong_Check(o)

from cpython cimport (
    PyNumber_Check as is_number,  # noqa: F401
    PyFloat_Check as is_float,  # noqa: F401
)

from cpython cimport PyNumber_Long as int  # noqa: F401

# Python strings:

from cpython cimport (
    PyUnicode_Check as is_unicode,  # noqa: F401
    PyBytes_Check as is_bytes,  # noqa: F401
)

from cpython cimport (
    PyUnicode_AsUTF8String as encode_utf8,  # noqa: F401
    PyUnicode_DecodeUTF8 as decode_utf8_ex,
    PyBytes_AsStringAndSize as bytes_to_charp,  # noqa: F401
    PyBytes_FromStringAndSize as charp_to_bytes,  # noqa: F401
)
cdef extern from 'Python.h':
    object charp_to_string 'PyUnicode_FromString'(char *v)

cdef object decode_utf8(const char *s):
    return decode_utf8_ex(s, strlen(s), NULL)

cdef extern from 'Python.h':
    int buffer_to_writable_memory 'PyObject_AsWriteBuffer'(object, void **, Py_ssize_t *)

# Python booleans:

from cpython cimport PyBool_FromLong as bool  # noqa: F401

# Python pointer->integer conversion:

from cpython cimport PyLong_FromVoidPtr as voidp_to_int  # noqa: F401

# Python files:

from libc.stdio cimport FILE  # noqa: F401

# Python lists:

from cpython cimport PyList_Append as list_append  # noqa: F401

# Python rich comparison:

from cpython cimport PyObject_RichCompare as richcmp  # noqa: F401

# Python slices:

cdef extern from 'Python.h':
    int is_slice 'PySlice_Check'(object)

# Python threads:

from cpython cimport (
    PyThread_type_lock as Lock,  # noqa: F401
    PyThread_allocate_lock as allocate_lock,  # noqa: F401
    PyThread_free_lock as free_lock,  # noqa: F401
    PyThread_acquire_lock as acquire_lock,  # noqa: F401
    PyThread_release_lock as release_lock,  # noqa: F401
    WAIT_LOCK,  # noqa: F401
    NOWAIT_LOCK,  # noqa: F401
)

# Python type checks:

cdef extern from 'object.h':
    ctypedef struct PyTypeObject:
        const char *tp_name

from cpython cimport PyObject
from cpython cimport PyObject_TypeCheck as _typecheck

cdef object type(object o):
    return <object>((<PyObject*>o).ob_type)

cdef object get_type_name(object type):
    return decode_utf8((<PyTypeObject*>type).tp_name)

cdef int typecheck(object o, object type):
    return _typecheck(o, <PyTypeObject*> type)

# Python exceptions:

cdef void raise_instantiation_error(object cls) except *:
    raise TypeError(f"cannot create '{get_type_name(cls)}' instances")
