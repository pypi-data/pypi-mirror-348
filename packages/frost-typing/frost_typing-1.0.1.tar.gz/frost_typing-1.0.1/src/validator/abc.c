#include "field.h"
#include "validator/validator.h"

TypeAdapter *TypeAdapter_AbcHashable, *TypeAdapter_AbcCallable,
  *TypeAdapter_AbcByteString;

static void
validator_iterable_dealloc(ValidatorIterable* self)
{
    Py_DECREF(self->ctx);
    Py_DECREF(self->iterator);
    Py_DECREF(self->validator);
    Py_TYPE(self)->tp_free(self);
}

static PyObject*
validator_iterable_repr(ValidatorIterable* self)
{
    return PyUnicode_FromFormat(
      "%s[%.100S]", Py_TYPE(self)->tp_name, self->validator);
}

static PyObject*
validator_iterable_next(ValidatorIterable* self)
{
    PyObject* items;
    int r = _PyIter_GetNext(self->iterator, &items);
    if (r != 1) {
        return NULL;
    }

    ValidateContext vctx =
      ValidateContext_Create(self->ctx, self, Py_TYPE(self), self->flags);
    PyObject* res = TypeAdapter_Conversion(self->validator, &vctx, items);
    if (!res) {
        ValidationError_Raise(
          NULL, self->validator, items, (PyObject*)Py_TYPE(self));
    }
    Py_DECREF(items);
    return res;
}

PyTypeObject ValidatorIterableType = {
    .tp_iternext = (iternextfunc)validator_iterable_next,
    .tp_dealloc = (destructor)validator_iterable_dealloc,
    .tp_repr = (reprfunc)validator_iterable_repr,
    .tp_name = "frost_typing.ValidatorIterable",
    .tp_basicsize = sizeof(ValidatorIterable),
    .tp_iter = PyObject_SelfIter,
};

PyObject*
ValidatorIterable_Create(PyObject* iterable,
                         ValidateContext* ctx,
                         TypeAdapter* validator)
{
    PyObject* iterator = PyObject_GetIter(iterable);
    if (!iterator) {
        return NULL;
    }

    ValidatorIterable* self =
      (ValidatorIterable*)ValidatorIterableType.tp_alloc(&ValidatorIterableType,
                                                         0);
    if (!self) {
        Py_DECREF(iterator);
        return NULL;
    }

    self->validator = (TypeAdapter*)Py_NewRef(validator);
    self->ctx = (ContextManager*)Py_NewRef(ctx->ctx);
    self->iterator = iterator;
    self->flags = ctx->flags;
    return (PyObject*)self;
};

static int
hashable_inspector(TypeAdapter* self, PyObject* val)
{
    return PyObject_CheckHashable(val);
}

static int
callable_inspector(TypeAdapter* self, PyObject* val)
{
    return PyCallable_Check(val);
}

static int
iterable_inspector(TypeAdapter* self, PyObject* val)
{
    return PyObject_CheckIter(val);
}

static PyObject*
iterable_convector(TypeAdapter* self, ValidateContext* ctx, PyObject* val)
{
    return ValidatorIterable_Create(val, ctx, (TypeAdapter*)self->args);
}

static int
sequence_inspector(TypeAdapter* self, PyObject* val)
{
    PySequenceMethods* tp_as_sequence = Py_TYPE(val)->tp_as_sequence;
    return tp_as_sequence && tp_as_sequence->sq_length &&
           tp_as_sequence->sq_item;
}

static int
byte_string_inspector(TypeAdapter* self, PyObject* val)
{
    return PyBytes_Check(val) || PyByteArray_Check(val);
}

static PyObject*
byte_string_converter(TypeAdapter* self, ValidateContext* ctx, PyObject* val)
{
    if ((ctx->flags & FIELD_STRICT) || !PyUnicode_Check(val)) {
        return NULL;
    }
    return PyUnicode_AsUTF8String(val);
}

static TypeAdapter*
type_adapter_create_iterable(PyObject* hint, PyObject* tp, PyObject* args)
{
    if (!args) {
        return TypeAdapter_Create(hint,
                                  NULL,
                                  NULL,
                                  TypeAdapter_Base_Repr,
                                  Not_Converter,
                                  iterable_inspector);
    }

    PyObject* vd = (PyObject*)ParseHint(PyTuple_GET_ITEM(args, 0), tp);
    if (!vd) {
        return NULL;
    }

    TypeAdapter* res = _TypeAdapter_NewCollection(hint, vd, iterable_convector);
    Py_DECREF(vd);
    return res;
}

TypeAdapter*
_TypeAdapter_CreateIterable(PyObject* cls, PyObject* tp, PyObject* args)
{
    if (args && !TypeAdapter_CollectionCheckArgs(args, (PyTypeObject*)cls, 1)) {
        return NULL;
    }
    return type_adapter_create_iterable(cls, tp, args);
}

TypeAdapter*
_TypeAdapter_CreateGenerator(PyObject* tp, PyObject* args)
{
    if (args && !TypeAdapter_CollectionCheckArgs(
                  args, (PyTypeObject*)AbcGenerator, 3)) {
        return NULL;
    }
    return type_adapter_create_iterable(AbcGenerator, tp, args);
}

TypeAdapter*
_TypeAdapter_CreateSequence(PyObject* tp, PyObject* args)
{
    if (!args) {
        return TypeAdapter_Create(AbcSequence,
                                  NULL,
                                  NULL,
                                  TypeAdapter_Base_Repr,
                                  Not_Converter,
                                  sequence_inspector);
    }
    return _TypeAdapter_Create_List(AbcSequence, args, tp);
}

int
abc_setup(void)
{
#define TYPE_ADAPTER_ABC(h, conv, ins)                                         \
    TypeAdapter_##h =                                                          \
      TypeAdapter_Create(h, NULL, NULL, TypeAdapter_Base_Repr, conv, ins);     \
    if (!TypeAdapter_##h) {                                                    \
        return -1;                                                             \
    }

    if (PyType_Ready(&ValidatorIterableType) < 0) {
        return -1;
    }

    TYPE_ADAPTER_ABC(AbcCallable, Not_Converter, callable_inspector);
    TYPE_ADAPTER_ABC(AbcHashable, Not_Converter, hashable_inspector);
    TYPE_ADAPTER_ABC(
      AbcByteString, byte_string_converter, byte_string_inspector);

#undef TYPE_ADAPTER_ABC
    return 0;
}

void
abc_free(void)
{
    Py_DECREF(TypeAdapter_AbcCallable);
    Py_DECREF(TypeAdapter_AbcHashable);
    Py_DECREF(TypeAdapter_AbcByteString);
}