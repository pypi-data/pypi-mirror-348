import sgqlc.types


auth_api_schema = sgqlc.types.Schema()



########################################################################
# Scalars and Enumerations
########################################################################
class AllowedFunctionsEnum(sgqlc.types.Enum):
    __schema__ = auth_api_schema
    __choices__ = ('Administration', 'Developer', 'EditCrawlers', 'EditDataImport', 'EditDocumentFeeds', 'EditExport', 'EditExternalSearch', 'EditKBAndDocuments', 'EditReferenceInfo', 'EditResearchMaps', 'EditStream', 'EditTransformations', 'ExportKBAndDocuments', 'ReadCrawlers', 'ReadDataImport', 'ReadDocumentFeeds', 'ReadExport', 'ReadExternalSearch', 'ReadKBAndDocuments', 'ReadReferenceInfo', 'ReadReportExport', 'ReadResearchMaps', 'ReadStream', 'ReadTransformations', 'RunCrawlers', 'RunDataImport', 'RunExternalSearch', 'RunTransformations', 'SourcesCustomizer', 'SourcesTechSupport', 'SourcesVerifier')


class AttributeSource(sgqlc.types.Enum):
    __schema__ = auth_api_schema
    __choices__ = ('Group', 'Personal')


class AttributeType(sgqlc.types.Enum):
    __schema__ = auth_api_schema
    __choices__ = ('boolean', 'booleanList', 'double', 'doubleList', 'int', 'intList', 'string', 'stringList')


Boolean = sgqlc.types.Boolean

Float = sgqlc.types.Float

ID = sgqlc.types.ID

Int = sgqlc.types.Int

class JSON(sgqlc.types.Scalar):
    __schema__ = auth_api_schema


class Long(sgqlc.types.Scalar):
    __schema__ = auth_api_schema


class PolicyIndex(sgqlc.types.Enum):
    __schema__ = auth_api_schema
    __choices__ = ('concepts', 'documents')


class PolicyType(sgqlc.types.Enum):
    __schema__ = auth_api_schema
    __choices__ = ('es', 'local')


String = sgqlc.types.String

class UnixTime(sgqlc.types.Scalar):
    __schema__ = auth_api_schema



########################################################################
# Input Objects
########################################################################
class AddUserGroupMembersParams(sgqlc.types.Input):
    __schema__ = auth_api_schema
    __field_names__ = ('group_ids', 'user_ids')
    group_ids = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(ID))), graphql_name='groupIds')
    user_ids = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(ID))), graphql_name='userIds')


class AttributeFilterSettings(sgqlc.types.Input):
    __schema__ = auth_api_schema
    __field_names__ = ('id', 'name')
    id = sgqlc.types.Field(String, graphql_name='id')
    name = sgqlc.types.Field(String, graphql_name='name')


class CreateUserGroupParams(sgqlc.types.Input):
    __schema__ = auth_api_schema
    __field_names__ = ('description', 'name')
    description = sgqlc.types.Field(String, graphql_name='description')
    name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='name')


class CreateUserParams(sgqlc.types.Input):
    __schema__ = auth_api_schema
    __field_names__ = ('access_level_id', 'email', 'enabled', 'fathers_name', 'first_name', 'last_name', 'login', 'receive_notifications', 'receive_telegram_notifications', 'telegram_chat_id')
    access_level_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='accessLevelID')
    email = sgqlc.types.Field(String, graphql_name='email')
    enabled = sgqlc.types.Field(Boolean, graphql_name='enabled')
    fathers_name = sgqlc.types.Field(String, graphql_name='fathersName')
    first_name = sgqlc.types.Field(String, graphql_name='firstName')
    last_name = sgqlc.types.Field(String, graphql_name='lastName')
    login = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='login')
    receive_notifications = sgqlc.types.Field(Boolean, graphql_name='receiveNotifications')
    receive_telegram_notifications = sgqlc.types.Field(Boolean, graphql_name='receiveTelegramNotifications')
    telegram_chat_id = sgqlc.types.Field(Long, graphql_name='telegramChatId')


class DeleteUserGroupMemberParams(sgqlc.types.Input):
    __schema__ = auth_api_schema
    __field_names__ = ('group_id', 'user_id')
    group_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='groupId')
    user_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='userId')


class PolicyParameterInputGQL(sgqlc.types.Input):
    __schema__ = auth_api_schema
    __field_names__ = ('param', 'parameter_type')
    param = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='param')
    parameter_type = sgqlc.types.Field(sgqlc.types.non_null(AttributeType), graphql_name='parameterType')


class SecurityPolicyArg(sgqlc.types.Input):
    __schema__ = auth_api_schema
    __field_names__ = ('id', 'index', 'name', 'params', 'policy_type', 'rule', 'target')
    id = sgqlc.types.Field(String, graphql_name='id')
    index = sgqlc.types.Field(PolicyIndex, graphql_name='index')
    name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='name')
    params = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(PolicyParameterInputGQL))), graphql_name='params')
    policy_type = sgqlc.types.Field(sgqlc.types.non_null(PolicyType), graphql_name='policyType')
    rule = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='rule')
    target = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='target')


class TimestampInterval(sgqlc.types.Input):
    __schema__ = auth_api_schema
    __field_names__ = ('end', 'start')
    end = sgqlc.types.Field(UnixTime, graphql_name='end')
    start = sgqlc.types.Field(UnixTime, graphql_name='start')


class UpdateCurrentUserParams(sgqlc.types.Input):
    __schema__ = auth_api_schema
    __field_names__ = ('email', 'fathers_name', 'first_name', 'last_name', 'password', 'receive_notifications', 'receive_telegram_notifications', 'telegram_chat_id')
    email = sgqlc.types.Field(String, graphql_name='email')
    fathers_name = sgqlc.types.Field(String, graphql_name='fathersName')
    first_name = sgqlc.types.Field(String, graphql_name='firstName')
    last_name = sgqlc.types.Field(String, graphql_name='lastName')
    password = sgqlc.types.Field(String, graphql_name='password')
    receive_notifications = sgqlc.types.Field(Boolean, graphql_name='receiveNotifications')
    receive_telegram_notifications = sgqlc.types.Field(Boolean, graphql_name='receiveTelegramNotifications')
    telegram_chat_id = sgqlc.types.Field(Long, graphql_name='telegramChatId')


class UpdateUserGroupParams(sgqlc.types.Input):
    __schema__ = auth_api_schema
    __field_names__ = ('description', 'name')
    description = sgqlc.types.Field(String, graphql_name='description')
    name = sgqlc.types.Field(String, graphql_name='name')


class UpdateUserParams(sgqlc.types.Input):
    __schema__ = auth_api_schema
    __field_names__ = ('access_level_id', 'email', 'enabled', 'fathers_name', 'first_name', 'last_name', 'receive_notifications', 'receive_telegram_notifications', 'telegram_chat_id')
    access_level_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='accessLevelID')
    email = sgqlc.types.Field(String, graphql_name='email')
    enabled = sgqlc.types.Field(Boolean, graphql_name='enabled')
    fathers_name = sgqlc.types.Field(String, graphql_name='fathersName')
    first_name = sgqlc.types.Field(String, graphql_name='firstName')
    last_name = sgqlc.types.Field(String, graphql_name='lastName')
    receive_notifications = sgqlc.types.Field(Boolean, graphql_name='receiveNotifications')
    receive_telegram_notifications = sgqlc.types.Field(Boolean, graphql_name='receiveTelegramNotifications')
    telegram_chat_id = sgqlc.types.Field(Long, graphql_name='telegramChatId')


class UserAttributeInput(sgqlc.types.Input):
    __schema__ = auth_api_schema
    __field_names__ = ('id', 'json_value')
    id = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='id')
    json_value = sgqlc.types.Field(sgqlc.types.non_null(JSON), graphql_name='jsonValue')


class UserFilterSettings(sgqlc.types.Input):
    __schema__ = auth_api_schema
    __field_names__ = ('creation_date', 'creator', 'email', 'enabled', 'fathers_name', 'first_name', 'group_ids', 'last_name', 'last_updater', 'login', 'query', 'show_system_users', 'update_date', 'user_id')
    creation_date = sgqlc.types.Field(TimestampInterval, graphql_name='creationDate')
    creator = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(ID)), graphql_name='creator')
    email = sgqlc.types.Field(String, graphql_name='email')
    enabled = sgqlc.types.Field(Boolean, graphql_name='enabled')
    fathers_name = sgqlc.types.Field(String, graphql_name='fathersName')
    first_name = sgqlc.types.Field(String, graphql_name='firstName')
    group_ids = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(ID)), graphql_name='groupIds')
    last_name = sgqlc.types.Field(String, graphql_name='lastName')
    last_updater = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(ID)), graphql_name='lastUpdater')
    login = sgqlc.types.Field(String, graphql_name='login')
    query = sgqlc.types.Field(String, graphql_name='query')
    show_system_users = sgqlc.types.Field(Boolean, graphql_name='showSystemUsers')
    update_date = sgqlc.types.Field(TimestampInterval, graphql_name='updateDate')
    user_id = sgqlc.types.Field(ID, graphql_name='userId')


class UserGroupFilterSettings(sgqlc.types.Input):
    __schema__ = auth_api_schema
    __field_names__ = ('creation_date', 'creator', 'description', 'last_updater', 'name', 'query', 'update_date', 'user_ids')
    creation_date = sgqlc.types.Field(TimestampInterval, graphql_name='creationDate')
    creator = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(ID)), graphql_name='creator')
    description = sgqlc.types.Field(String, graphql_name='description')
    last_updater = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(ID)), graphql_name='lastUpdater')
    name = sgqlc.types.Field(String, graphql_name='name')
    query = sgqlc.types.Field(String, graphql_name='query')
    update_date = sgqlc.types.Field(TimestampInterval, graphql_name='updateDate')
    user_ids = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(ID)), graphql_name='userIds')



########################################################################
# Output Objects and Interfaces
########################################################################
class RecordInterface(sgqlc.types.Interface):
    __schema__ = auth_api_schema
    __field_names__ = ('creator', 'last_updater', 'system_registration_date', 'system_update_date')
    creator = sgqlc.types.Field(sgqlc.types.non_null('User'), graphql_name='creator')
    last_updater = sgqlc.types.Field('User', graphql_name='lastUpdater')
    system_registration_date = sgqlc.types.Field(sgqlc.types.non_null(UnixTime), graphql_name='systemRegistrationDate')
    system_update_date = sgqlc.types.Field(UnixTime, graphql_name='systemUpdateDate')


class AccessLevel(sgqlc.types.Type):
    __schema__ = auth_api_schema
    __field_names__ = ('id', 'name', 'order')
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='id')
    name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='name')
    order = sgqlc.types.Field(sgqlc.types.non_null(Long), graphql_name='order')


class Attribute(sgqlc.types.Type):
    __schema__ = auth_api_schema
    __field_names__ = ('id', 'name', 'params_schema', 'value_type')
    id = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='id')
    name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='name')
    params_schema = sgqlc.types.Field(sgqlc.types.non_null('ParamsSchema'), graphql_name='paramsSchema')
    value_type = sgqlc.types.Field(sgqlc.types.non_null(AttributeType), graphql_name='valueType')


class AttributePagination(sgqlc.types.Type):
    __schema__ = auth_api_schema
    __field_names__ = ('list_attribute', 'total')
    list_attribute = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(Attribute))), graphql_name='listAttribute')
    total = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='total')


class BooleanListValue(sgqlc.types.Type):
    __schema__ = auth_api_schema
    __field_names__ = ('value',)
    value = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(Boolean))), graphql_name='value')


class BooleanValue(sgqlc.types.Type):
    __schema__ = auth_api_schema
    __field_names__ = ('value',)
    value = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='value')


class ConflictsState(sgqlc.types.Type):
    __schema__ = auth_api_schema
    __field_names__ = ('group_conflicts', 'user_conflicts')
    group_conflicts = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(Boolean)), graphql_name='groupConflicts')
    user_conflicts = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(Boolean)), graphql_name='userConflicts')


class DoubleListValue(sgqlc.types.Type):
    __schema__ = auth_api_schema
    __field_names__ = ('value',)
    value = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(Float))), graphql_name='value')


class DoubleValue(sgqlc.types.Type):
    __schema__ = auth_api_schema
    __field_names__ = ('value',)
    value = sgqlc.types.Field(sgqlc.types.non_null(Float), graphql_name='value')


class IntListValue(sgqlc.types.Type):
    __schema__ = auth_api_schema
    __field_names__ = ('value',)
    value = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(Int))), graphql_name='value')


class IntValue(sgqlc.types.Type):
    __schema__ = auth_api_schema
    __field_names__ = ('value',)
    value = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='value')


class Mutation(sgqlc.types.Type):
    __schema__ = auth_api_schema
    __field_names__ = ('add_policy', 'add_user', 'add_user_group', 'add_user_group_members', 'delete_kvstore_item', 'delete_policy', 'delete_user', 'delete_user_group', 'delete_user_group_members', 'set_kvstore_item', 'update_current_user', 'update_current_user_password', 'update_user', 'update_user_activity', 'update_user_attributes', 'update_user_group', 'update_user_group_attributes', 'update_user_password')
    add_policy = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='addPolicy', args=sgqlc.types.ArgDict((
        ('policy_params', sgqlc.types.Arg(sgqlc.types.non_null(SecurityPolicyArg), graphql_name='policyParams', default=None)),
))
    )
    add_user = sgqlc.types.Field('User', graphql_name='addUser', args=sgqlc.types.ArgDict((
        ('create_user_params', sgqlc.types.Arg(sgqlc.types.non_null(CreateUserParams), graphql_name='createUserParams', default=None)),
))
    )
    add_user_group = sgqlc.types.Field('UserGroup', graphql_name='addUserGroup', args=sgqlc.types.ArgDict((
        ('create_user_group_params', sgqlc.types.Arg(sgqlc.types.non_null(CreateUserGroupParams), graphql_name='createUserGroupParams', default=None)),
))
    )
    add_user_group_members = sgqlc.types.Field(sgqlc.types.non_null('StateWithError'), graphql_name='addUserGroupMembers', args=sgqlc.types.ArgDict((
        ('add_user_group_members_params', sgqlc.types.Arg(sgqlc.types.non_null(AddUserGroupMembersParams), graphql_name='addUserGroupMembersParams', default=None)),
))
    )
    delete_kvstore_item = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='deleteKVStoreItem', args=sgqlc.types.ArgDict((
        ('key', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='key', default=None)),
))
    )
    delete_policy = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='deletePolicy', args=sgqlc.types.ArgDict((
        ('id', sgqlc.types.Arg(sgqlc.types.non_null(ID), graphql_name='id', default=None)),
))
    )
    delete_user = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='deleteUser', args=sgqlc.types.ArgDict((
        ('id', sgqlc.types.Arg(sgqlc.types.non_null(ID), graphql_name='id', default=None)),
))
    )
    delete_user_group = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='deleteUserGroup', args=sgqlc.types.ArgDict((
        ('id', sgqlc.types.Arg(sgqlc.types.non_null(ID), graphql_name='id', default=None)),
))
    )
    delete_user_group_members = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='deleteUserGroupMembers', args=sgqlc.types.ArgDict((
        ('delete_user_group_member_params', sgqlc.types.Arg(sgqlc.types.non_null(DeleteUserGroupMemberParams), graphql_name='deleteUserGroupMemberParams', default=None)),
))
    )
    set_kvstore_item = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='setKVStoreItem', args=sgqlc.types.ArgDict((
        ('key', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='key', default=None)),
        ('value', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='value', default=None)),
))
    )
    update_current_user = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='updateCurrentUser', args=sgqlc.types.ArgDict((
        ('update_current_user_params', sgqlc.types.Arg(sgqlc.types.non_null(UpdateCurrentUserParams), graphql_name='updateCurrentUserParams', default=None)),
))
    )
    update_current_user_password = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='updateCurrentUserPassword', args=sgqlc.types.ArgDict((
        ('old_password', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='oldPassword', default=None)),
        ('password', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='password', default=None)),
))
    )
    update_user = sgqlc.types.Field('User', graphql_name='updateUser', args=sgqlc.types.ArgDict((
        ('id', sgqlc.types.Arg(sgqlc.types.non_null(ID), graphql_name='id', default=None)),
        ('update_user_params', sgqlc.types.Arg(sgqlc.types.non_null(UpdateUserParams), graphql_name='updateUserParams', default=None)),
))
    )
    update_user_activity = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='updateUserActivity', args=sgqlc.types.ArgDict((
        ('ids', sgqlc.types.Arg(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(ID))), graphql_name='ids', default=None)),
        ('is_enabled', sgqlc.types.Arg(sgqlc.types.non_null(Boolean), graphql_name='isEnabled', default=None)),
))
    )
    update_user_attributes = sgqlc.types.Field(sgqlc.types.non_null('UserWithError'), graphql_name='updateUserAttributes', args=sgqlc.types.ArgDict((
        ('attributes', sgqlc.types.Arg(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(UserAttributeInput))), graphql_name='attributes', default=None)),
        ('id', sgqlc.types.Arg(sgqlc.types.non_null(ID), graphql_name='id', default=None)),
))
    )
    update_user_group = sgqlc.types.Field(sgqlc.types.non_null('UserGroup'), graphql_name='updateUserGroup', args=sgqlc.types.ArgDict((
        ('id', sgqlc.types.Arg(sgqlc.types.non_null(ID), graphql_name='id', default=None)),
        ('update_user_group_params', sgqlc.types.Arg(sgqlc.types.non_null(UpdateUserGroupParams), graphql_name='updateUserGroupParams', default=None)),
))
    )
    update_user_group_attributes = sgqlc.types.Field(sgqlc.types.non_null('UserGroupWithError'), graphql_name='updateUserGroupAttributes', args=sgqlc.types.ArgDict((
        ('attributes', sgqlc.types.Arg(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(UserAttributeInput))), graphql_name='attributes', default=None)),
        ('id', sgqlc.types.Arg(sgqlc.types.non_null(ID), graphql_name='id', default=None)),
))
    )
    update_user_password = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='updateUserPassword', args=sgqlc.types.ArgDict((
        ('id', sgqlc.types.Arg(sgqlc.types.non_null(ID), graphql_name='id', default=None)),
        ('password', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='password', default=None)),
))
    )


class ParamsSchema(sgqlc.types.Type):
    __schema__ = auth_api_schema
    __field_names__ = ('schema', 'ui_schema')
    schema = sgqlc.types.Field(sgqlc.types.non_null(JSON), graphql_name='schema')
    ui_schema = sgqlc.types.Field(JSON, graphql_name='uiSchema')


class PolicyParameterGQL(sgqlc.types.Type):
    __schema__ = auth_api_schema
    __field_names__ = ('param', 'parameter_type')
    param = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='param')
    parameter_type = sgqlc.types.Field(sgqlc.types.non_null(AttributeType), graphql_name='parameterType')


class Query(sgqlc.types.Type):
    __schema__ = auth_api_schema
    __field_names__ = ('current_user', 'get_kvstore_item', 'list_policy', 'pagination_attribute', 'pagination_user', 'pagination_user_group', 'refresh_token', 'token_exchange', 'user', 'user_by_login', 'user_group', 'user_idlist', 'user_idlist_sys', 'user_sys')
    current_user = sgqlc.types.Field(sgqlc.types.non_null('User'), graphql_name='currentUser')
    get_kvstore_item = sgqlc.types.Field(String, graphql_name='getKVStoreItem', args=sgqlc.types.ArgDict((
        ('key', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='key', default=None)),
))
    )
    list_policy = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null('SecurityPolicyGQL'))), graphql_name='listPolicy', args=sgqlc.types.ArgDict((
        ('ids', sgqlc.types.Arg(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(ID))), graphql_name='ids', default=None)),
))
    )
    pagination_attribute = sgqlc.types.Field(sgqlc.types.non_null(AttributePagination), graphql_name='paginationAttribute', args=sgqlc.types.ArgDict((
        ('attribute_filter_settings', sgqlc.types.Arg(sgqlc.types.non_null(AttributeFilterSettings), graphql_name='attributeFilterSettings', default=None)),
        ('limit', sgqlc.types.Arg(Int, graphql_name='limit', default=20)),
        ('offset', sgqlc.types.Arg(Int, graphql_name='offset', default=0)),
        ('query', sgqlc.types.Arg(String, graphql_name='query', default=None)),
))
    )
    pagination_user = sgqlc.types.Field(sgqlc.types.non_null('UserPagination'), graphql_name='paginationUser', args=sgqlc.types.ArgDict((
        ('filter_settings', sgqlc.types.Arg(sgqlc.types.non_null(UserFilterSettings), graphql_name='filterSettings', default=None)),
        ('limit', sgqlc.types.Arg(Int, graphql_name='limit', default=20)),
        ('offset', sgqlc.types.Arg(Int, graphql_name='offset', default=0)),
))
    )
    pagination_user_group = sgqlc.types.Field(sgqlc.types.non_null('UserGroupPagination'), graphql_name='paginationUserGroup', args=sgqlc.types.ArgDict((
        ('filter_settings', sgqlc.types.Arg(sgqlc.types.non_null(UserGroupFilterSettings), graphql_name='filterSettings', default=None)),
        ('limit', sgqlc.types.Arg(Int, graphql_name='limit', default=20)),
        ('offset', sgqlc.types.Arg(Int, graphql_name='offset', default=0)),
))
    )
    refresh_token = sgqlc.types.Field('Token', graphql_name='refreshToken', args=sgqlc.types.ArgDict((
        ('refresh_token', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='refreshToken', default=None)),
))
    )
    token_exchange = sgqlc.types.Field('Token', graphql_name='tokenExchange', args=sgqlc.types.ArgDict((
        ('id', sgqlc.types.Arg(sgqlc.types.non_null(ID), graphql_name='id', default=None)),
))
    )
    user = sgqlc.types.Field('User', graphql_name='user', args=sgqlc.types.ArgDict((
        ('id', sgqlc.types.Arg(sgqlc.types.non_null(ID), graphql_name='id', default=None)),
))
    )
    user_by_login = sgqlc.types.Field(sgqlc.types.non_null('User'), graphql_name='userByLogin', args=sgqlc.types.ArgDict((
        ('password', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='password', default=None)),
        ('username', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='username', default=None)),
))
    )
    user_group = sgqlc.types.Field(sgqlc.types.non_null('UserGroup'), graphql_name='userGroup', args=sgqlc.types.ArgDict((
        ('id', sgqlc.types.Arg(sgqlc.types.non_null(ID), graphql_name='id', default=None)),
))
    )
    user_idlist = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of('User')), graphql_name='userIDList', args=sgqlc.types.ArgDict((
        ('ids', sgqlc.types.Arg(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(ID))), graphql_name='ids', default=None)),
))
    )
    user_idlist_sys = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of('User')), graphql_name='userIDListSys', args=sgqlc.types.ArgDict((
        ('ids', sgqlc.types.Arg(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(ID))), graphql_name='ids', default=None)),
))
    )
    user_sys = sgqlc.types.Field('User', graphql_name='userSys', args=sgqlc.types.ArgDict((
        ('id', sgqlc.types.Arg(sgqlc.types.non_null(ID), graphql_name='id', default=None)),
))
    )


class SecurityPolicyGQL(sgqlc.types.Type):
    __schema__ = auth_api_schema
    __field_names__ = ('id', 'index', 'name', 'params', 'policy_type', 'rule', 'target')
    id = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='id')
    index = sgqlc.types.Field(PolicyIndex, graphql_name='index')
    name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='name')
    params = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(PolicyParameterGQL))), graphql_name='params')
    policy_type = sgqlc.types.Field(sgqlc.types.non_null(PolicyType), graphql_name='policyType')
    rule = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='rule')
    target = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='target')


class StateWithError(sgqlc.types.Type):
    __schema__ = auth_api_schema
    __field_names__ = ('info', 'state')
    info = sgqlc.types.Field(sgqlc.types.non_null(ConflictsState), graphql_name='info')
    state = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='state')


class StringListValue(sgqlc.types.Type):
    __schema__ = auth_api_schema
    __field_names__ = ('value',)
    value = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(String))), graphql_name='value')


class StringValue(sgqlc.types.Type):
    __schema__ = auth_api_schema
    __field_names__ = ('value',)
    value = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='value')


class Token(sgqlc.types.Type):
    __schema__ = auth_api_schema
    __field_names__ = ('access_token', 'access_token_expires_at', 'refresh_token', 'refresh_token_expires_at')
    access_token = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='accessToken')
    access_token_expires_at = sgqlc.types.Field(sgqlc.types.non_null(Long), graphql_name='accessTokenExpiresAt')
    refresh_token = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='refreshToken')
    refresh_token_expires_at = sgqlc.types.Field(sgqlc.types.non_null(Long), graphql_name='refreshTokenExpiresAt')


class UserAttribute(sgqlc.types.Type):
    __schema__ = auth_api_schema
    __field_names__ = ('attribute_source', 'id', 'json_value', 'name', 'value')
    attribute_source = sgqlc.types.Field(sgqlc.types.non_null(AttributeSource), graphql_name='attributeSource')
    id = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='id')
    json_value = sgqlc.types.Field(sgqlc.types.non_null(JSON), graphql_name='jsonValue')
    name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='name')
    value = sgqlc.types.Field(sgqlc.types.non_null('AttributeValue'), graphql_name='value')


class UserGroupMetrics(sgqlc.types.Type):
    __schema__ = auth_api_schema
    __field_names__ = ('count_user',)
    count_user = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='countUser')


class UserGroupPagination(sgqlc.types.Type):
    __schema__ = auth_api_schema
    __field_names__ = ('list_user_group', 'total')
    list_user_group = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null('UserGroup'))), graphql_name='listUserGroup')
    total = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='total')


class UserGroupWithError(sgqlc.types.Type):
    __schema__ = auth_api_schema
    __field_names__ = ('info', 'user_group')
    info = sgqlc.types.Field(sgqlc.types.non_null(ConflictsState), graphql_name='info')
    user_group = sgqlc.types.Field(sgqlc.types.non_null('UserGroup'), graphql_name='userGroup')


class UserMetrics(sgqlc.types.Type):
    __schema__ = auth_api_schema
    __field_names__ = ('count_group',)
    count_group = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='countGroup')


class UserPagination(sgqlc.types.Type):
    __schema__ = auth_api_schema
    __field_names__ = ('list_user', 'total')
    list_user = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null('User'))), graphql_name='listUser')
    total = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='total')


class UserWithError(sgqlc.types.Type):
    __schema__ = auth_api_schema
    __field_names__ = ('info', 'user')
    info = sgqlc.types.Field(sgqlc.types.non_null(ConflictsState), graphql_name='info')
    user = sgqlc.types.Field(sgqlc.types.non_null('User'), graphql_name='user')


class User(sgqlc.types.Type, RecordInterface):
    __schema__ = auth_api_schema
    __field_names__ = ('access_level', 'allowed_functions', 'attributes', 'email', 'enabled', 'fathers_name', 'first_name', 'id', 'is_admin', 'last_name', 'list_user_group', 'login', 'metrics', 'name', 'receive_notifications', 'receive_telegram_notifications', 'telegram_chat_id')
    access_level = sgqlc.types.Field(sgqlc.types.non_null(AccessLevel), graphql_name='accessLevel')
    allowed_functions = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(AllowedFunctionsEnum))), graphql_name='allowedFunctions')
    attributes = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(UserAttribute))), graphql_name='attributes', args=sgqlc.types.ArgDict((
        ('is_request_from_front', sgqlc.types.Arg(Boolean, graphql_name='isRequestFromFront', default=True)),
        ('show_default', sgqlc.types.Arg(Boolean, graphql_name='showDefault', default=False)),
))
    )
    email = sgqlc.types.Field(String, graphql_name='email')
    enabled = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='enabled')
    fathers_name = sgqlc.types.Field(String, graphql_name='fathersName')
    first_name = sgqlc.types.Field(String, graphql_name='firstName')
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='id')
    is_admin = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='isAdmin')
    last_name = sgqlc.types.Field(String, graphql_name='lastName')
    list_user_group = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null('UserGroup'))), graphql_name='listUserGroup')
    login = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='login')
    metrics = sgqlc.types.Field(sgqlc.types.non_null(UserMetrics), graphql_name='metrics')
    name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='name')
    receive_notifications = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='receiveNotifications')
    receive_telegram_notifications = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='receiveTelegramNotifications')
    telegram_chat_id = sgqlc.types.Field(Long, graphql_name='telegramChatId')


class UserGroup(sgqlc.types.Type, RecordInterface):
    __schema__ = auth_api_schema
    __field_names__ = ('attributes', 'description', 'id', 'list_user', 'metrics', 'name')
    attributes = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(UserAttribute))), graphql_name='attributes')
    description = sgqlc.types.Field(String, graphql_name='description')
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='id')
    list_user = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(User))), graphql_name='listUser')
    metrics = sgqlc.types.Field(sgqlc.types.non_null(UserGroupMetrics), graphql_name='metrics')
    name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='name')



########################################################################
# Unions
########################################################################
class AttributeValue(sgqlc.types.Union):
    __schema__ = auth_api_schema
    __types__ = (BooleanListValue, BooleanValue, DoubleListValue, DoubleValue, IntListValue, IntValue, StringListValue, StringValue)



########################################################################
# Schema Entry Points
########################################################################
auth_api_schema.query_type = Query
auth_api_schema.mutation_type = Mutation
auth_api_schema.subscription_type = None

