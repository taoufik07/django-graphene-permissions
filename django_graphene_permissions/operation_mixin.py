class OperationHolderMixin:
    def __and__(self, other):
        return OperandHolder(AND, self, other)

    def __or__(self, other):
        return OperandHolder(OR, self, other)

    def __rand__(self, other):
        return OperandHolder(AND, other, self)

    def __ror__(self, other):
        return OperandHolder(OR, other, self)

    def __invert__(self):
        return SingleOperandHolder(NOT, self)


class SingleOperandHolder(OperationHolderMixin):
    def __init__(self, operator_class, op1_class):
        self.operator_class = operator_class
        self.op1_class = op1_class

    def __call__(self, *args, **kwargs):
        op1 = self.op1_class(*args, **kwargs)
        return self.operator_class(op1)


class OperandHolder(OperationHolderMixin):
    def __init__(self, operator_class, op1_class, op2_class):
        self.operator_class = operator_class
        self.op1_class = op1_class
        self.op2_class = op2_class

    def __call__(self, *args, **kwargs):
        op1 = self.op1_class(*args, **kwargs)
        op2 = self.op2_class(*args, **kwargs)
        return self.operator_class(op1, op2)


class AND:
    def __init__(self, op1, op2):
        self.op1 = op1
        self.op2 = op2

    def has_permission(self, context):
        return (
                self.op1.has_permission(context) and
                self.op2.has_permission(context)
        )

    def has_object_permission(self, context, obj):
        return (
                self.op1.has_object_permission(context, obj) and
                self.op2.has_object_permission(context, obj)
        )


class OR:
    def __init__(self, op1, op2):
        self.op1 = op1
        self.op2 = op2

    def has_permission(self, context):
        return (
                self.op1.has_permission(context) or
                self.op2.has_permission(context)
        )

    def has_object_permission(self, context, obj):
        return (
                self.op1.has_object_permission(context, obj) or
                self.op2.has_object_permission(context, obj)
        )


class NOT:
    def __init__(self, op1):
        self.op1 = op1

    def has_permission(self, context):
        return not self.op1.has_permission(context)

    def has_object_permission(self, context, obj):
        return not self.op1.has_object_permission(context, obj)


class BasePermissionMetaclass(OperationHolderMixin, type):
    pass
