import sgqlc.types


crawlers_api_schema = sgqlc.types.Schema()



########################################################################
# Scalars and Enumerations
########################################################################
Boolean = sgqlc.types.Boolean

class CollectionStatus(sgqlc.types.Enum):
    __schema__ = crawlers_api_schema
    __choices__ = ('Canceled', 'Error', 'InProgress', 'Pending', 'Success', 'WithMistakes')


class CrawlStateSorting(sgqlc.types.Enum):
    __schema__ = crawlers_api_schema
    __choices__ = ('crawlKey', 'creatorId', 'id', 'lastUpdaterId', 'systemRegistrationDate', 'systemUpdateDate')


class CrawlerSorting(sgqlc.types.Enum):
    __schema__ = crawlers_api_schema
    __choices__ = ('avgPerformanceTime', 'id', 'lastCollectionDate', 'projectTitle', 'title')


class CrawlerType(sgqlc.types.Enum):
    __schema__ = crawlers_api_schema
    __choices__ = ('Emulator', 'Search', 'Target')


class CredentialSorting(sgqlc.types.Enum):
    __schema__ = crawlers_api_schema
    __choices__ = ('dataType', 'domain', 'id', 'status', 'value')


class CredentialStatus(sgqlc.types.Enum):
    __schema__ = crawlers_api_schema
    __choices__ = ('Invalid', 'Valid')


class CredentialType(sgqlc.types.Enum):
    __schema__ = crawlers_api_schema
    __choices__ = ('Account', 'Token')


class DeployStatus(sgqlc.types.Enum):
    __schema__ = crawlers_api_schema
    __choices__ = ('Error', 'InProgress', 'NothingToDeploy', 'Success')


class DistributionType(sgqlc.types.Enum):
    __schema__ = crawlers_api_schema
    __choices__ = ('EggFile', 'External', 'Sitemap')


class EventTarget(sgqlc.types.Enum):
    __schema__ = crawlers_api_schema
    __choices__ = ('crawlersApi',)


Float = sgqlc.types.Float

ID = sgqlc.types.ID

class InformationSourceLoaderActualStatus(sgqlc.types.Enum):
    __schema__ = crawlers_api_schema
    __choices__ = ('Daily', 'EveryTwoDays', 'Never', 'TwiceADay', 'Weekly')


class InformationSourceLoaderSorting(sgqlc.types.Enum):
    __schema__ = crawlers_api_schema
    __choices__ = ('id', 'status')


class InformationSourceSorting(sgqlc.types.Enum):
    __schema__ = crawlers_api_schema
    __choices__ = ('error', 'id', 'job', 'siteName', 'status', 'url')


Int = sgqlc.types.Int

class JSON(sgqlc.types.Scalar):
    __schema__ = crawlers_api_schema


class JobPriorityType(sgqlc.types.Enum):
    __schema__ = crawlers_api_schema
    __choices__ = ('High', 'Highest', 'Low', 'Normal')


class JobSorting(sgqlc.types.Enum):
    __schema__ = crawlers_api_schema
    __choices__ = ('args', 'collectionStatus', 'crawlerName', 'creator', 'endTime', 'id', 'jobPriority', 'periodicJobId', 'projectName', 'queueTime', 'settings', 'startTime', 'systemRegistrationDate')


class JobStatus(sgqlc.types.Enum):
    __schema__ = crawlers_api_schema
    __choices__ = ('Finished', 'Paused', 'Pending', 'Running')


class LogLevel(sgqlc.types.Enum):
    __schema__ = crawlers_api_schema
    __choices__ = ('Critical', 'Debug', 'Error', 'Info', 'Trace', 'Warning')


class LogSorting(sgqlc.types.Enum):
    __schema__ = crawlers_api_schema
    __choices__ = ('level', 'timestamp')


class Long(sgqlc.types.Scalar):
    __schema__ = crawlers_api_schema


class MessagePriority(sgqlc.types.Enum):
    __schema__ = crawlers_api_schema
    __choices__ = ('Background', 'High', 'Normal', 'VeryHigh')


class MetricSorting(sgqlc.types.Enum):
    __schema__ = crawlers_api_schema
    __choices__ = ('timestamp',)


class MonitoringStatus(sgqlc.types.Enum):
    __schema__ = crawlers_api_schema
    __choices__ = ('Critical', 'Ok', 'Pending', 'SameItemsJob', 'SameItemsPeriodic', 'ZeroItemsZeroDuplicates')


class PeriodicJobSorting(sgqlc.types.Enum):
    __schema__ = crawlers_api_schema
    __choices__ = ('crawlerId', 'crawlerName', 'creator', 'credentialId', 'id', 'lastUpdater', 'name', 'nextScheduleTime', 'priority', 'projectId', 'projectName', 'status', 'systemRegistrationDate', 'systemUpdateDate')


class ProjectSorting(sgqlc.types.Enum):
    __schema__ = crawlers_api_schema
    __choices__ = ('creator', 'description', 'id', 'lastUpdater', 'name', 'systemRegistrationDate', 'systemUpdateDate', 'title')


class RecoveryJobSorting(sgqlc.types.Enum):
    __schema__ = crawlers_api_schema
    __choices__ = ('createdAt', 'endTime', 'id', 'progress', 'startTime', 'status', 'updatedAt')


class RecoveryJobStatus(sgqlc.types.Enum):
    __schema__ = crawlers_api_schema
    __choices__ = ('Canceled', 'Error', 'InProgress', 'Pending', 'Success')


class RequestSorting(sgqlc.types.Enum):
    __schema__ = crawlers_api_schema
    __choices__ = ('timestamp',)


class RunningStatus(sgqlc.types.Enum):
    __schema__ = crawlers_api_schema
    __choices__ = ('Disabled', 'Enabled')


class SettingsType(sgqlc.types.Enum):
    __schema__ = crawlers_api_schema
    __choices__ = ('array', 'boolean', 'float', 'int', 'object', 'string')


class SortDirection(sgqlc.types.Enum):
    __schema__ = crawlers_api_schema
    __choices__ = ('ascending', 'descending')


String = sgqlc.types.String

class TypeOfCrawl(sgqlc.types.Enum):
    __schema__ = crawlers_api_schema
    __choices__ = ('Actual', 'Retrospective')


class UnixTime(sgqlc.types.Scalar):
    __schema__ = crawlers_api_schema


class VersionSorting(sgqlc.types.Enum):
    __schema__ = crawlers_api_schema
    __choices__ = ('id', 'systemRegistrationDate', 'versionName')


class VersionStatus(sgqlc.types.Enum):
    __schema__ = crawlers_api_schema
    __choices__ = ('Active', 'Outdated', 'Removed')



########################################################################
# Input Objects
########################################################################
class AddCrawlStateInput(sgqlc.types.Input):
    __schema__ = crawlers_api_schema
    __field_names__ = ('cookie', 'parameters', 'state')
    cookie = sgqlc.types.Field(JSON, graphql_name='cookie')
    parameters = sgqlc.types.Field(sgqlc.types.non_null('CrawlStateParameters'), graphql_name='parameters')
    state = sgqlc.types.Field(sgqlc.types.non_null(JSON), graphql_name='state')


class AddRecoveryJobInput(sgqlc.types.Input):
    __schema__ = crawlers_api_schema
    __field_names__ = ('crawler_id', 'version_id')
    crawler_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='crawlerId')
    version_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='versionId')


class CancelJobInput(sgqlc.types.Input):
    __schema__ = crawlers_api_schema
    __field_names__ = ('ids', 'status')
    ids = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(ID)), graphql_name='ids')
    status = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(JobStatus)), graphql_name='status')


class CrawlStateFilterSettings(sgqlc.types.Input):
    __schema__ = crawlers_api_schema
    __field_names__ = ('crawler_ids', 'creator_ids', 'credential_ids', 'information_source_ids', 'input_value', 'last_updater_ids', 'periodic_job_ids', 'system_registration_date', 'system_update_date')
    crawler_ids = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(ID)), graphql_name='crawlerIds')
    creator_ids = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(String)), graphql_name='creatorIds')
    credential_ids = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(ID)), graphql_name='credentialIds')
    information_source_ids = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(ID)), graphql_name='informationSourceIds')
    input_value = sgqlc.types.Field(String, graphql_name='inputValue')
    last_updater_ids = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(String)), graphql_name='lastUpdaterIds')
    periodic_job_ids = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(ID)), graphql_name='periodicJobIds')
    system_registration_date = sgqlc.types.Field('TimestampInterval', graphql_name='systemRegistrationDate')
    system_update_date = sgqlc.types.Field('TimestampInterval', graphql_name='systemUpdateDate')


class CrawlStateParameters(sgqlc.types.Input):
    __schema__ = crawlers_api_schema
    __field_names__ = ('crawl_key', 'crawler_id', 'credential_id', 'information_source_id', 'periodic_job_id')
    crawl_key = sgqlc.types.Field(String, graphql_name='crawlKey')
    crawler_id = sgqlc.types.Field(ID, graphql_name='crawlerId')
    credential_id = sgqlc.types.Field(ID, graphql_name='credentialId')
    information_source_id = sgqlc.types.Field(ID, graphql_name='informationSourceId')
    periodic_job_id = sgqlc.types.Field(ID, graphql_name='periodicJobId')


class CrawlerFilterSettings(sgqlc.types.Input):
    __schema__ = crawlers_api_schema
    __field_names__ = ('crawler_types', 'creators', 'distribution_types', 'have_active_versions', 'input_value', 'last_collection_date', 'projects', 'system_registration_date', 'system_update_date', 'updaters')
    crawler_types = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(CrawlerType)), graphql_name='crawlerTypes')
    creators = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(String)), graphql_name='creators')
    distribution_types = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(DistributionType)), graphql_name='distributionTypes')
    have_active_versions = sgqlc.types.Field(Boolean, graphql_name='haveActiveVersions')
    input_value = sgqlc.types.Field(String, graphql_name='inputValue')
    last_collection_date = sgqlc.types.Field('TimestampInterval', graphql_name='lastCollectionDate')
    projects = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(ID)), graphql_name='projects')
    system_registration_date = sgqlc.types.Field('TimestampInterval', graphql_name='systemRegistrationDate')
    system_update_date = sgqlc.types.Field('TimestampInterval', graphql_name='systemUpdateDate')
    updaters = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(String)), graphql_name='updaters')


class CrawlerUpdateInput(sgqlc.types.Input):
    __schema__ = crawlers_api_schema
    __field_names__ = ('args', 'description', 'project_id', 'settings', 'title')
    args = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null('KeyValueInputType'))), graphql_name='args')
    description = sgqlc.types.Field(String, graphql_name='description')
    project_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='projectId')
    settings = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null('KeyValueInputType'))), graphql_name='settings')
    title = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='title')


class CredentialFilterSettings(sgqlc.types.Input):
    __schema__ = crawlers_api_schema
    __field_names__ = ('creators', 'data_type', 'input_value', 'projects', 'status', 'system_registration_date', 'system_update_date', 'updaters')
    creators = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(String)), graphql_name='creators')
    data_type = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(CredentialType)), graphql_name='dataType')
    input_value = sgqlc.types.Field(String, graphql_name='inputValue')
    projects = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(ID)), graphql_name='projects')
    status = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(CredentialStatus)), graphql_name='status')
    system_registration_date = sgqlc.types.Field('TimestampInterval', graphql_name='systemRegistrationDate')
    system_update_date = sgqlc.types.Field('TimestampInterval', graphql_name='systemUpdateDate')
    updaters = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(String)), graphql_name='updaters')


class CredentialInput(sgqlc.types.Input):
    __schema__ = crawlers_api_schema
    __field_names__ = ('data_type', 'description', 'domain', 'login', 'password', 'projects', 'status', 'token')
    data_type = sgqlc.types.Field(sgqlc.types.non_null(CredentialType), graphql_name='dataType')
    description = sgqlc.types.Field(String, graphql_name='description')
    domain = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='domain')
    login = sgqlc.types.Field(String, graphql_name='login')
    password = sgqlc.types.Field(String, graphql_name='password')
    projects = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(ID))), graphql_name='projects')
    status = sgqlc.types.Field(CredentialStatus, graphql_name='status')
    token = sgqlc.types.Field(String, graphql_name='token')


class InformationSourceFilterSettings(sgqlc.types.Input):
    __schema__ = crawlers_api_schema
    __field_names__ = ('information_source_id', 'input_value', 'status')
    information_source_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='informationSourceId')
    input_value = sgqlc.types.Field(String, graphql_name='inputValue')
    status = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(CollectionStatus)), graphql_name='status')


class InformationSourceLoaderFilterSettings(sgqlc.types.Input):
    __schema__ = crawlers_api_schema
    __field_names__ = ('creators', 'input_value', 'status', 'system_registration_date', 'system_update_date', 'type_of_crawl', 'updaters')
    creators = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(String)), graphql_name='creators')
    input_value = sgqlc.types.Field(String, graphql_name='inputValue')
    status = sgqlc.types.Field(CollectionStatus, graphql_name='status')
    system_registration_date = sgqlc.types.Field('TimestampInterval', graphql_name='systemRegistrationDate')
    system_update_date = sgqlc.types.Field('TimestampInterval', graphql_name='systemUpdateDate')
    type_of_crawl = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(TypeOfCrawl)), graphql_name='typeOfCrawl')
    updaters = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(String)), graphql_name='updaters')


class InformationSourceLoaderInput(sgqlc.types.Input):
    __schema__ = crawlers_api_schema
    __field_names__ = ('actual_status', 'file_settings', 'is_retrospective', 'retrospective_interval', 'running_status', 'urls')
    actual_status = sgqlc.types.Field(InformationSourceLoaderActualStatus, graphql_name='actualStatus')
    file_settings = sgqlc.types.Field('S3FileSettings', graphql_name='fileSettings')
    is_retrospective = sgqlc.types.Field(Boolean, graphql_name='isRetrospective')
    retrospective_interval = sgqlc.types.Field('TimestampInterval', graphql_name='retrospectiveInterval')
    running_status = sgqlc.types.Field(RunningStatus, graphql_name='runningStatus')
    urls = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null('KeyOptionValueInput')), graphql_name='urls')


class JobInput(sgqlc.types.Input):
    __schema__ = crawlers_api_schema
    __field_names__ = ('args', 'crawler_id', 'credential_id', 'external_search_loader_id', 'is_noise', 'message_priority', 'priority', 'research_map_id', 'settings', 'version_id')
    args = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null('KeyValueInputType'))), graphql_name='args')
    crawler_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='crawlerId')
    credential_id = sgqlc.types.Field(ID, graphql_name='credentialId')
    external_search_loader_id = sgqlc.types.Field(ID, graphql_name='externalSearchLoaderId')
    is_noise = sgqlc.types.Field(Boolean, graphql_name='isNoise')
    message_priority = sgqlc.types.Field(MessagePriority, graphql_name='messagePriority')
    priority = sgqlc.types.Field(sgqlc.types.non_null(JobPriorityType), graphql_name='priority')
    research_map_id = sgqlc.types.Field(ID, graphql_name='researchMapId')
    settings = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null('KeyValueInputType'))), graphql_name='settings')
    version_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='versionId')


class JobsFilterSettings(sgqlc.types.Input):
    __schema__ = crawlers_api_schema
    __field_names__ = ('collection_statuses', 'crawlers', 'creators', 'end_time', 'input_value', 'job_ids', 'job_statuses', 'periodic_jobs', 'projects', 'start_time', 'system_registration_date', 'system_update_date', 'updaters')
    collection_statuses = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(CollectionStatus)), graphql_name='collectionStatuses')
    crawlers = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(ID)), graphql_name='crawlers')
    creators = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(String)), graphql_name='creators')
    end_time = sgqlc.types.Field('TimestampInterval', graphql_name='endTime')
    input_value = sgqlc.types.Field(String, graphql_name='inputValue')
    job_ids = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(ID)), graphql_name='jobIds')
    job_statuses = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(JobStatus)), graphql_name='jobStatuses')
    periodic_jobs = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(ID)), graphql_name='periodicJobs')
    projects = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(ID)), graphql_name='projects')
    start_time = sgqlc.types.Field('TimestampInterval', graphql_name='startTime')
    system_registration_date = sgqlc.types.Field('TimestampInterval', graphql_name='systemRegistrationDate')
    system_update_date = sgqlc.types.Field('TimestampInterval', graphql_name='systemUpdateDate')
    updaters = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(String)), graphql_name='updaters')


class KeyOptionValueInput(sgqlc.types.Input):
    __schema__ = crawlers_api_schema
    __field_names__ = ('key', 'value')
    key = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='key')
    value = sgqlc.types.Field(String, graphql_name='value')


class KeyValueInputType(sgqlc.types.Input):
    __schema__ = crawlers_api_schema
    __field_names__ = ('key', 'value')
    key = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='key')
    value = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='value')


class LogFilterSettings(sgqlc.types.Input):
    __schema__ = crawlers_api_schema
    __field_names__ = ('input_text', 'interval', 'levels')
    input_text = sgqlc.types.Field(String, graphql_name='inputText')
    interval = sgqlc.types.Field('TimestampInterval', graphql_name='interval')
    levels = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(LogLevel)), graphql_name='levels')


class MetricFilterSettings(sgqlc.types.Input):
    __schema__ = crawlers_api_schema
    __field_names__ = ('input_text', 'interval')
    input_text = sgqlc.types.Field(String, graphql_name='inputText')
    interval = sgqlc.types.Field('TimestampInterval', graphql_name='interval')


class PeriodicJobFilterSettings(sgqlc.types.Input):
    __schema__ = crawlers_api_schema
    __field_names__ = ('crawlers', 'creators', 'input_value', 'next_schedule_time', 'priorities', 'projects', 'running_statuses', 'system_registration_date', 'system_update_date', 'updaters')
    crawlers = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(ID)), graphql_name='crawlers')
    creators = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(String)), graphql_name='creators')
    input_value = sgqlc.types.Field(String, graphql_name='inputValue')
    next_schedule_time = sgqlc.types.Field('TimestampInterval', graphql_name='nextScheduleTime')
    priorities = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(JobPriorityType)), graphql_name='priorities')
    projects = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(ID)), graphql_name='projects')
    running_statuses = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(RunningStatus)), graphql_name='runningStatuses')
    system_registration_date = sgqlc.types.Field('TimestampInterval', graphql_name='systemRegistrationDate')
    system_update_date = sgqlc.types.Field('TimestampInterval', graphql_name='systemUpdateDate')
    updaters = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(String)), graphql_name='updaters')


class PeriodicJobInput(sgqlc.types.Input):
    __schema__ = crawlers_api_schema
    __field_names__ = ('args', 'crawler_id', 'credential_id', 'cron_expression', 'cron_utcoffset_minutes', 'description', 'disable_time', 'message_priority', 'priority', 'settings', 'status', 'title', 'update_on_reload', 'version_id')
    args = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(KeyValueInputType))), graphql_name='args')
    crawler_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='crawlerId')
    credential_id = sgqlc.types.Field(ID, graphql_name='credentialId')
    cron_expression = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='cronExpression')
    cron_utcoffset_minutes = sgqlc.types.Field(Int, graphql_name='cronUTCOffsetMinutes')
    description = sgqlc.types.Field(String, graphql_name='description')
    disable_time = sgqlc.types.Field(UnixTime, graphql_name='disableTime')
    message_priority = sgqlc.types.Field(MessagePriority, graphql_name='messagePriority')
    priority = sgqlc.types.Field(JobPriorityType, graphql_name='priority')
    settings = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(KeyValueInputType))), graphql_name='settings')
    status = sgqlc.types.Field(RunningStatus, graphql_name='status')
    title = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='title')
    update_on_reload = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='updateOnReload')
    version_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='versionId')


class ProjectFilterSettings(sgqlc.types.Input):
    __schema__ = crawlers_api_schema
    __field_names__ = ('creators', 'input_value', 'name', 'system_registration_date', 'system_update_date', 'updaters')
    creators = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(String)), graphql_name='creators')
    input_value = sgqlc.types.Field(String, graphql_name='inputValue')
    name = sgqlc.types.Field(String, graphql_name='name')
    system_registration_date = sgqlc.types.Field('TimestampInterval', graphql_name='systemRegistrationDate')
    system_update_date = sgqlc.types.Field('TimestampInterval', graphql_name='systemUpdateDate')
    updaters = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(String)), graphql_name='updaters')


class ProjectInput(sgqlc.types.Input):
    __schema__ = crawlers_api_schema
    __field_names__ = ('args', 'description', 'name', 's3_file', 'settings', 'title')
    args = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(KeyValueInputType))), graphql_name='args')
    description = sgqlc.types.Field(String, graphql_name='description')
    name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='name')
    s3_file = sgqlc.types.Field('S3FileInput', graphql_name='s3File')
    settings = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(KeyValueInputType))), graphql_name='settings')
    title = sgqlc.types.Field(String, graphql_name='title')


class RecoveryJobFilterSettings(sgqlc.types.Input):
    __schema__ = crawlers_api_schema
    __field_names__ = ('crawlers', 'created_at', 'creators', 'end_time', 'input_value', 'start_time', 'statuses', 'updated_at', 'updaters')
    crawlers = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(ID)), graphql_name='crawlers')
    created_at = sgqlc.types.Field('TimestampInterval', graphql_name='createdAt')
    creators = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(String)), graphql_name='creators')
    end_time = sgqlc.types.Field('TimestampInterval', graphql_name='endTime')
    input_value = sgqlc.types.Field(String, graphql_name='inputValue')
    start_time = sgqlc.types.Field('TimestampInterval', graphql_name='startTime')
    statuses = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(RecoveryJobStatus)), graphql_name='statuses')
    updated_at = sgqlc.types.Field('TimestampInterval', graphql_name='updatedAt')
    updaters = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(String)), graphql_name='updaters')


class RequestFilterSettings(sgqlc.types.Input):
    __schema__ = crawlers_api_schema
    __field_names__ = ('input_text', 'interval')
    input_text = sgqlc.types.Field(String, graphql_name='inputText')
    interval = sgqlc.types.Field('TimestampInterval', graphql_name='interval')


class S3FileInput(sgqlc.types.Input):
    __schema__ = crawlers_api_schema
    __field_names__ = ('bucket_name', 'object_name')
    bucket_name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='bucketName')
    object_name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='objectName')


class S3FileSettings(sgqlc.types.Input):
    __schema__ = crawlers_api_schema
    __field_names__ = ('is_first_row_title', 'is_site_name_not_exist', 's3_file')
    is_first_row_title = sgqlc.types.Field(Boolean, graphql_name='isFirstRowTitle')
    is_site_name_not_exist = sgqlc.types.Field(Boolean, graphql_name='isSiteNameNotExist')
    s3_file = sgqlc.types.Field(sgqlc.types.non_null(S3FileInput), graphql_name='s3File')


class TimestampInterval(sgqlc.types.Input):
    __schema__ = crawlers_api_schema
    __field_names__ = ('end', 'start')
    end = sgqlc.types.Field(UnixTime, graphql_name='end')
    start = sgqlc.types.Field(UnixTime, graphql_name='start')


class UpdateCrawlStateInput(sgqlc.types.Input):
    __schema__ = crawlers_api_schema
    __field_names__ = ('cookie', 'credential_status', 'state', 'state_version')
    cookie = sgqlc.types.Field(JSON, graphql_name='cookie')
    credential_status = sgqlc.types.Field(CredentialStatus, graphql_name='credentialStatus')
    state = sgqlc.types.Field(sgqlc.types.non_null(JSON), graphql_name='state')
    state_version = sgqlc.types.Field(sgqlc.types.non_null(Long), graphql_name='stateVersion')


class VersionFilterSettings(sgqlc.types.Input):
    __schema__ = crawlers_api_schema
    __field_names__ = ('input_value', 'with_removed_versions')
    input_value = sgqlc.types.Field(String, graphql_name='inputValue')
    with_removed_versions = sgqlc.types.Field(Boolean, graphql_name='withRemovedVersions')



########################################################################
# Output Objects and Interfaces
########################################################################
class RecordInterface(sgqlc.types.Interface):
    __schema__ = crawlers_api_schema
    __field_names__ = ('creator', 'last_updater', 'system_registration_date', 'system_update_date')
    creator = sgqlc.types.Field(sgqlc.types.non_null('User'), graphql_name='creator')
    last_updater = sgqlc.types.Field('User', graphql_name='lastUpdater')
    system_registration_date = sgqlc.types.Field(sgqlc.types.non_null(UnixTime), graphql_name='systemRegistrationDate')
    system_update_date = sgqlc.types.Field(UnixTime, graphql_name='systemUpdateDate')


class ArgsAndSettingsDescription(sgqlc.types.Type):
    __schema__ = crawlers_api_schema
    __field_names__ = ('args', 'settings')
    args = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null('SettingDescription')), graphql_name='args')
    settings = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null('SettingDescription')), graphql_name='settings')


class CrawlStatePagination(sgqlc.types.Type):
    __schema__ = crawlers_api_schema
    __field_names__ = ('list_crawl_state', 'total')
    list_crawl_state = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null('CrawlState'))), graphql_name='listCrawlState')
    total = sgqlc.types.Field(sgqlc.types.non_null(Long), graphql_name='total')


class CrawlerHistogram(sgqlc.types.Type):
    __schema__ = crawlers_api_schema
    __field_names__ = ('canceled_job_count', 'crawler_name', 'error_job_count', 'items_scraped_count', 'jobs_count', 'successful_job_count', 'with_mistakes')
    canceled_job_count = sgqlc.types.Field(Int, graphql_name='canceledJobCount')
    crawler_name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='crawlerName')
    error_job_count = sgqlc.types.Field(Int, graphql_name='errorJobCount')
    items_scraped_count = sgqlc.types.Field(Long, graphql_name='itemsScrapedCount')
    jobs_count = sgqlc.types.Field(Int, graphql_name='jobsCount')
    successful_job_count = sgqlc.types.Field(Int, graphql_name='successfulJobCount')
    with_mistakes = sgqlc.types.Field(Int, graphql_name='withMistakes')


class CrawlerPagination(sgqlc.types.Type):
    __schema__ = crawlers_api_schema
    __field_names__ = ('list_crawler', 'total')
    list_crawler = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null('Crawler'))), graphql_name='listCrawler')
    total = sgqlc.types.Field(sgqlc.types.non_null(Long), graphql_name='total')


class CrawlerStats(sgqlc.types.Type):
    __schema__ = crawlers_api_schema
    __field_names__ = ('avg_performance_time', 'items_scraped_count', 'items_scraped_count_last', 'last_collection_date', 'next_schedule_time', 'total_time')
    avg_performance_time = sgqlc.types.Field(Long, graphql_name='avgPerformanceTime')
    items_scraped_count = sgqlc.types.Field(Long, graphql_name='itemsScrapedCount')
    items_scraped_count_last = sgqlc.types.Field(Long, graphql_name='itemsScrapedCountLast')
    last_collection_date = sgqlc.types.Field(UnixTime, graphql_name='lastCollectionDate')
    next_schedule_time = sgqlc.types.Field(UnixTime, graphql_name='nextScheduleTime')
    total_time = sgqlc.types.Field(Long, graphql_name='totalTime')


class CredentialPagination(sgqlc.types.Type):
    __schema__ = crawlers_api_schema
    __field_names__ = ('list_credential', 'total')
    list_credential = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null('Credential'))), graphql_name='listCredential')
    total = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='total')


class DateHistogramBucket(sgqlc.types.Type):
    __schema__ = crawlers_api_schema
    __field_names__ = ('date', 'doc_count', 'timestamp')
    date = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='date')
    doc_count = sgqlc.types.Field(sgqlc.types.non_null(Long), graphql_name='docCount')
    timestamp = sgqlc.types.Field(sgqlc.types.non_null(Long), graphql_name='timestamp')


class Event(sgqlc.types.Type):
    __schema__ = crawlers_api_schema
    __field_names__ = ('id', 'is_read', 'message', 'target')
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='id')
    is_read = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='isRead')
    message = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='message')
    target = sgqlc.types.Field(sgqlc.types.non_null(EventTarget), graphql_name='target')


class InformationSource(sgqlc.types.Type):
    __schema__ = crawlers_api_schema
    __field_names__ = ('crawler', 'error_message', 'id', 'job', 'periodic_job', 'site_name', 'status', 'url', 'version')
    crawler = sgqlc.types.Field('Crawler', graphql_name='crawler')
    error_message = sgqlc.types.Field(String, graphql_name='errorMessage')
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='id')
    job = sgqlc.types.Field('Job', graphql_name='job')
    periodic_job = sgqlc.types.Field('PeriodicJob', graphql_name='periodicJob')
    site_name = sgqlc.types.Field(String, graphql_name='siteName')
    status = sgqlc.types.Field(sgqlc.types.non_null(CollectionStatus), graphql_name='status')
    url = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='url')
    version = sgqlc.types.Field('Version', graphql_name='version')


class InformationSourceLoaderFileTitle(sgqlc.types.Type):
    __schema__ = crawlers_api_schema
    __field_names__ = ('title',)
    title = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='title')


class InformationSourceLoaderPagination(sgqlc.types.Type):
    __schema__ = crawlers_api_schema
    __field_names__ = ('list_information_source_loader', 'total')
    list_information_source_loader = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null('InformationSourceLoader'))), graphql_name='listInformationSourceLoader')
    total = sgqlc.types.Field(sgqlc.types.non_null(Long), graphql_name='total')


class InformationSourceLoaderStats(sgqlc.types.Type):
    __schema__ = crawlers_api_schema
    __field_names__ = ('finished_source_count', 'total_source_count')
    finished_source_count = sgqlc.types.Field(sgqlc.types.non_null(Long), graphql_name='finishedSourceCount')
    total_source_count = sgqlc.types.Field(sgqlc.types.non_null(Long), graphql_name='totalSourceCount')


class InformationSourceLoaderURLTitle(sgqlc.types.Type):
    __schema__ = crawlers_api_schema
    __field_names__ = ('source_count', 'title')
    source_count = sgqlc.types.Field(sgqlc.types.non_null(Long), graphql_name='sourceCount')
    title = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='title')


class InformationSourcePagination(sgqlc.types.Type):
    __schema__ = crawlers_api_schema
    __field_names__ = ('list_information_source', 'total')
    list_information_source = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(InformationSource))), graphql_name='listInformationSource')
    total = sgqlc.types.Field(sgqlc.types.non_null(Long), graphql_name='total')


class JobMetrics(sgqlc.types.Type):
    __schema__ = crawlers_api_schema
    __field_names__ = ('job_id',)
    job_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='jobId')


class JobPagination(sgqlc.types.Type):
    __schema__ = crawlers_api_schema
    __field_names__ = ('list_job', 'total')
    list_job = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null('Job'))), graphql_name='listJob')
    total = sgqlc.types.Field(sgqlc.types.non_null(Long), graphql_name='total')


class JobStats(sgqlc.types.Type):
    __schema__ = crawlers_api_schema
    __field_names__ = ('canceled_job_count', 'duplicated_request_count', 'error_job_count', 'errors_count', 'items_scraped_count', 'jobs_count', 'requests_count', 'successful_job_count', 'total_time', 'with_mistakes')
    canceled_job_count = sgqlc.types.Field(Int, graphql_name='canceledJobCount')
    duplicated_request_count = sgqlc.types.Field(Int, graphql_name='duplicatedRequestCount')
    error_job_count = sgqlc.types.Field(Int, graphql_name='errorJobCount')
    errors_count = sgqlc.types.Field(Int, graphql_name='errorsCount')
    items_scraped_count = sgqlc.types.Field(Long, graphql_name='itemsScrapedCount')
    jobs_count = sgqlc.types.Field(Int, graphql_name='jobsCount')
    requests_count = sgqlc.types.Field(Long, graphql_name='requestsCount')
    successful_job_count = sgqlc.types.Field(Int, graphql_name='successfulJobCount')
    total_time = sgqlc.types.Field(Long, graphql_name='totalTime')
    with_mistakes = sgqlc.types.Field(Int, graphql_name='withMistakes')


class JobSubscription(sgqlc.types.Type):
    __schema__ = crawlers_api_schema
    __field_names__ = ('job', 'position')
    job = sgqlc.types.Field(sgqlc.types.non_null('Job'), graphql_name='job')
    position = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='position')


class KeyValue(sgqlc.types.Type):
    __schema__ = crawlers_api_schema
    __field_names__ = ('key', 'value')
    key = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='key')
    value = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='value')


class Log(sgqlc.types.Type):
    __schema__ = crawlers_api_schema
    __field_names__ = ('job_id', 'level', 'logger_name', 'message', 'stack_trace', 'timestamp')
    job_id = sgqlc.types.Field(String, graphql_name='jobId')
    level = sgqlc.types.Field(sgqlc.types.non_null(LogLevel), graphql_name='level')
    logger_name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='loggerName')
    message = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='message')
    stack_trace = sgqlc.types.Field(String, graphql_name='stackTrace')
    timestamp = sgqlc.types.Field(sgqlc.types.non_null(UnixTime), graphql_name='timestamp')


class LogPagination(sgqlc.types.Type):
    __schema__ = crawlers_api_schema
    __field_names__ = ('list_log', 'total')
    list_log = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(Log))), graphql_name='listLog')
    total = sgqlc.types.Field(sgqlc.types.non_null(Long), graphql_name='total')


class Metric(sgqlc.types.Type):
    __schema__ = crawlers_api_schema
    __field_names__ = ('job_id', 'metric', 'timestamp')
    job_id = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='jobId')
    metric = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='metric')
    timestamp = sgqlc.types.Field(sgqlc.types.non_null(UnixTime), graphql_name='timestamp')


class MetricPagination(sgqlc.types.Type):
    __schema__ = crawlers_api_schema
    __field_names__ = ('list_metric', 'total')
    list_metric = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(Metric))), graphql_name='listMetric')
    total = sgqlc.types.Field(sgqlc.types.non_null(Long), graphql_name='total')


class Mutation(sgqlc.types.Type):
    __schema__ = crawlers_api_schema
    __field_names__ = ('add_crawl_state', 'add_credential', 'add_information_source_loader', 'add_job', 'add_periodic_job', 'add_project', 'add_recovery_job', 'cancel_job', 'cancel_recovery_job', 'delete_crawl_state', 'delete_crawler_versions', 'delete_crawlers', 'delete_credential', 'delete_information_source_loader', 'delete_job', 'delete_periodic_job', 'delete_project', 'delete_project_versions', 'download_pending_jobs', 'import_periodic_jobs', 'restart_job', 'resume_job', 'run_periodic_jobs', 'schedule_uploaded_jobs', 'suspend_job', 'update_crawl_state', 'update_crawler', 'update_crawler_settings_arguments', 'update_credential', 'update_disable_information_source_loader', 'update_disable_jobs_scheduling', 'update_enable_information_source_loader', 'update_enable_jobs_scheduling', 'update_periodic_job', 'update_periodic_job_settings_and_arguments', 'update_project', 'update_project_settings_and_arguments', 'update_site_map_crawler_body')
    add_crawl_state = sgqlc.types.Field(sgqlc.types.non_null('CrawlState'), graphql_name='addCrawlState', args=sgqlc.types.ArgDict((
        ('add_crawl_state_input', sgqlc.types.Arg(sgqlc.types.non_null(AddCrawlStateInput), graphql_name='addCrawlStateInput', default=None)),
))
    )
    add_credential = sgqlc.types.Field(sgqlc.types.non_null('Credential'), graphql_name='addCredential', args=sgqlc.types.ArgDict((
        ('credential_input', sgqlc.types.Arg(sgqlc.types.non_null(CredentialInput), graphql_name='credentialInput', default=None)),
))
    )
    add_information_source_loader = sgqlc.types.Field(sgqlc.types.non_null('InformationSourceLoader'), graphql_name='addInformationSourceLoader', args=sgqlc.types.ArgDict((
        ('information_source_loader_input', sgqlc.types.Arg(sgqlc.types.non_null(InformationSourceLoaderInput), graphql_name='informationSourceLoaderInput', default=None)),
))
    )
    add_job = sgqlc.types.Field(sgqlc.types.non_null('Job'), graphql_name='addJob', args=sgqlc.types.ArgDict((
        ('job_input', sgqlc.types.Arg(sgqlc.types.non_null(JobInput), graphql_name='jobInput', default=None)),
))
    )
    add_periodic_job = sgqlc.types.Field(sgqlc.types.non_null('PeriodicJob'), graphql_name='addPeriodicJob', args=sgqlc.types.ArgDict((
        ('periodic_job_input', sgqlc.types.Arg(sgqlc.types.non_null(PeriodicJobInput), graphql_name='periodicJobInput', default=None)),
))
    )
    add_project = sgqlc.types.Field(sgqlc.types.non_null('Project'), graphql_name='addProject', args=sgqlc.types.ArgDict((
        ('project_input', sgqlc.types.Arg(sgqlc.types.non_null(ProjectInput), graphql_name='projectInput', default=None)),
))
    )
    add_recovery_job = sgqlc.types.Field(sgqlc.types.non_null('RecoveryJob'), graphql_name='addRecoveryJob', args=sgqlc.types.ArgDict((
        ('add_recovery_job_input', sgqlc.types.Arg(sgqlc.types.non_null(AddRecoveryJobInput), graphql_name='addRecoveryJobInput', default=None)),
))
    )
    cancel_job = sgqlc.types.Field(sgqlc.types.non_null('State'), graphql_name='cancelJob', args=sgqlc.types.ArgDict((
        ('cancel_job_input', sgqlc.types.Arg(CancelJobInput, graphql_name='cancelJobInput', default={'ids': (), 'status': ()})),
))
    )
    cancel_recovery_job = sgqlc.types.Field(sgqlc.types.non_null('RecoveryJob'), graphql_name='cancelRecoveryJob', args=sgqlc.types.ArgDict((
        ('id', sgqlc.types.Arg(sgqlc.types.non_null(ID), graphql_name='id', default=None)),
))
    )
    delete_crawl_state = sgqlc.types.Field(sgqlc.types.non_null('State'), graphql_name='deleteCrawlState', args=sgqlc.types.ArgDict((
        ('crawl_id', sgqlc.types.Arg(sgqlc.types.non_null(ID), graphql_name='crawlId', default=None)),
))
    )
    delete_crawler_versions = sgqlc.types.Field(sgqlc.types.non_null('State'), graphql_name='deleteCrawlerVersions', args=sgqlc.types.ArgDict((
        ('crawler_id', sgqlc.types.Arg(sgqlc.types.non_null(ID), graphql_name='crawlerId', default=None)),
        ('version_ids', sgqlc.types.Arg(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(ID))), graphql_name='versionIds', default=None)),
))
    )
    delete_crawlers = sgqlc.types.Field(sgqlc.types.non_null('State'), graphql_name='deleteCrawlers', args=sgqlc.types.ArgDict((
        ('ids', sgqlc.types.Arg(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(ID))), graphql_name='ids', default=None)),
))
    )
    delete_credential = sgqlc.types.Field(sgqlc.types.non_null('State'), graphql_name='deleteCredential', args=sgqlc.types.ArgDict((
        ('ids', sgqlc.types.Arg(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(ID))), graphql_name='ids', default=None)),
))
    )
    delete_information_source_loader = sgqlc.types.Field(sgqlc.types.non_null('State'), graphql_name='deleteInformationSourceLoader', args=sgqlc.types.ArgDict((
        ('ids', sgqlc.types.Arg(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(ID))), graphql_name='ids', default=None)),
))
    )
    delete_job = sgqlc.types.Field(sgqlc.types.non_null('State'), graphql_name='deleteJob', args=sgqlc.types.ArgDict((
        ('ids', sgqlc.types.Arg(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(ID))), graphql_name='ids', default=None)),
))
    )
    delete_periodic_job = sgqlc.types.Field(sgqlc.types.non_null('State'), graphql_name='deletePeriodicJob', args=sgqlc.types.ArgDict((
        ('ids', sgqlc.types.Arg(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(ID))), graphql_name='ids', default=None)),
))
    )
    delete_project = sgqlc.types.Field(sgqlc.types.non_null('State'), graphql_name='deleteProject', args=sgqlc.types.ArgDict((
        ('ids', sgqlc.types.Arg(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(ID))), graphql_name='ids', default=None)),
))
    )
    delete_project_versions = sgqlc.types.Field(sgqlc.types.non_null('State'), graphql_name='deleteProjectVersions', args=sgqlc.types.ArgDict((
        ('ids', sgqlc.types.Arg(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(ID))), graphql_name='ids', default=None)),
        ('project_id', sgqlc.types.Arg(sgqlc.types.non_null(ID), graphql_name='projectId', default=None)),
))
    )
    download_pending_jobs = sgqlc.types.Field(sgqlc.types.non_null(JSON), graphql_name='downloadPendingJobs')
    import_periodic_jobs = sgqlc.types.Field(sgqlc.types.non_null('State'), graphql_name='importPeriodicJobs', args=sgqlc.types.ArgDict((
        ('s3_file_input', sgqlc.types.Arg(sgqlc.types.non_null(S3FileInput), graphql_name='s3FileInput', default=None)),
))
    )
    restart_job = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null('Job'))), graphql_name='restartJob', args=sgqlc.types.ArgDict((
        ('ids', sgqlc.types.Arg(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(ID))), graphql_name='ids', default=None)),
))
    )
    resume_job = sgqlc.types.Field(sgqlc.types.non_null('State'), graphql_name='resumeJob', args=sgqlc.types.ArgDict((
        ('ids', sgqlc.types.Arg(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(ID))), graphql_name='ids', default=None)),
))
    )
    run_periodic_jobs = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null('Job'))), graphql_name='runPeriodicJobs', args=sgqlc.types.ArgDict((
        ('periodic_job_ids', sgqlc.types.Arg(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(ID))), graphql_name='periodicJobIds', default=None)),
))
    )
    schedule_uploaded_jobs = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null('Job'))), graphql_name='scheduleUploadedJobs', args=sgqlc.types.ArgDict((
        ('s3_file_input', sgqlc.types.Arg(sgqlc.types.non_null(S3FileInput), graphql_name='s3FileInput', default=None)),
))
    )
    suspend_job = sgqlc.types.Field(sgqlc.types.non_null('State'), graphql_name='suspendJob', args=sgqlc.types.ArgDict((
        ('ids', sgqlc.types.Arg(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(ID))), graphql_name='ids', default=None)),
))
    )
    update_crawl_state = sgqlc.types.Field(sgqlc.types.non_null('CrawlState'), graphql_name='updateCrawlState', args=sgqlc.types.ArgDict((
        ('crawl_id', sgqlc.types.Arg(sgqlc.types.non_null(ID), graphql_name='crawlId', default=None)),
        ('update_crawl_state_input', sgqlc.types.Arg(sgqlc.types.non_null(UpdateCrawlStateInput), graphql_name='updateCrawlStateInput', default=None)),
))
    )
    update_crawler = sgqlc.types.Field(sgqlc.types.non_null('Crawler'), graphql_name='updateCrawler', args=sgqlc.types.ArgDict((
        ('crawler_id', sgqlc.types.Arg(sgqlc.types.non_null(ID), graphql_name='crawlerId', default=None)),
        ('crawler_update_input', sgqlc.types.Arg(sgqlc.types.non_null(CrawlerUpdateInput), graphql_name='crawlerUpdateInput', default=None)),
        ('project_id', sgqlc.types.Arg(sgqlc.types.non_null(ID), graphql_name='projectId', default=None)),
))
    )
    update_crawler_settings_arguments = sgqlc.types.Field(sgqlc.types.non_null('Crawler'), graphql_name='updateCrawlerSettingsArguments', args=sgqlc.types.ArgDict((
        ('args', sgqlc.types.Arg(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(KeyValueInputType))), graphql_name='args', default=None)),
        ('crawler_id', sgqlc.types.Arg(sgqlc.types.non_null(ID), graphql_name='crawlerId', default=None)),
        ('settings', sgqlc.types.Arg(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(KeyValueInputType))), graphql_name='settings', default=None)),
))
    )
    update_credential = sgqlc.types.Field(sgqlc.types.non_null('Credential'), graphql_name='updateCredential', args=sgqlc.types.ArgDict((
        ('credential_input', sgqlc.types.Arg(sgqlc.types.non_null(CredentialInput), graphql_name='credentialInput', default=None)),
        ('id', sgqlc.types.Arg(sgqlc.types.non_null(ID), graphql_name='id', default=None)),
        ('version', sgqlc.types.Arg(sgqlc.types.non_null(Int), graphql_name='version', default=None)),
))
    )
    update_disable_information_source_loader = sgqlc.types.Field(sgqlc.types.non_null('State'), graphql_name='updateDisableInformationSourceLoader', args=sgqlc.types.ArgDict((
        ('ids', sgqlc.types.Arg(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(ID))), graphql_name='ids', default=None)),
))
    )
    update_disable_jobs_scheduling = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null('PeriodicJob'))), graphql_name='updateDisableJobsScheduling', args=sgqlc.types.ArgDict((
        ('ids', sgqlc.types.Arg(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(ID))), graphql_name='ids', default=None)),
))
    )
    update_enable_information_source_loader = sgqlc.types.Field(sgqlc.types.non_null('State'), graphql_name='updateEnableInformationSourceLoader', args=sgqlc.types.ArgDict((
        ('ids', sgqlc.types.Arg(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(ID))), graphql_name='ids', default=None)),
))
    )
    update_enable_jobs_scheduling = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null('PeriodicJob'))), graphql_name='updateEnableJobsScheduling', args=sgqlc.types.ArgDict((
        ('ids', sgqlc.types.Arg(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(ID))), graphql_name='ids', default=None)),
))
    )
    update_periodic_job = sgqlc.types.Field(sgqlc.types.non_null('PeriodicJob'), graphql_name='updatePeriodicJob', args=sgqlc.types.ArgDict((
        ('id', sgqlc.types.Arg(sgqlc.types.non_null(ID), graphql_name='id', default=None)),
        ('periodic_job_input', sgqlc.types.Arg(sgqlc.types.non_null(PeriodicJobInput), graphql_name='periodicJobInput', default=None)),
))
    )
    update_periodic_job_settings_and_arguments = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='updatePeriodicJobSettingsAndArguments', args=sgqlc.types.ArgDict((
        ('args', sgqlc.types.Arg(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(KeyValueInputType))), graphql_name='args', default=None)),
        ('id', sgqlc.types.Arg(sgqlc.types.non_null(ID), graphql_name='id', default=None)),
        ('settings', sgqlc.types.Arg(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(KeyValueInputType))), graphql_name='settings', default=None)),
))
    )
    update_project = sgqlc.types.Field(sgqlc.types.non_null('Project'), graphql_name='updateProject', args=sgqlc.types.ArgDict((
        ('id', sgqlc.types.Arg(sgqlc.types.non_null(ID), graphql_name='id', default=None)),
        ('project_input', sgqlc.types.Arg(sgqlc.types.non_null(ProjectInput), graphql_name='projectInput', default=None)),
))
    )
    update_project_settings_and_arguments = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='updateProjectSettingsAndArguments', args=sgqlc.types.ArgDict((
        ('args', sgqlc.types.Arg(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(KeyValueInputType))), graphql_name='args', default=None)),
        ('id', sgqlc.types.Arg(sgqlc.types.non_null(ID), graphql_name='id', default=None)),
        ('settings', sgqlc.types.Arg(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(KeyValueInputType))), graphql_name='settings', default=None)),
))
    )
    update_site_map_crawler_body = sgqlc.types.Field(sgqlc.types.non_null('Crawler'), graphql_name='updateSiteMapCrawlerBody', args=sgqlc.types.ArgDict((
        ('crawler_id', sgqlc.types.Arg(sgqlc.types.non_null(ID), graphql_name='crawlerId', default=None)),
        ('json', sgqlc.types.Arg(sgqlc.types.non_null(JSON), graphql_name='json', default=None)),
        ('project_id', sgqlc.types.Arg(sgqlc.types.non_null(ID), graphql_name='projectId', default=None)),
))
    )


class PeriodicJobMetrics(sgqlc.types.Type):
    __schema__ = crawlers_api_schema
    __field_names__ = ('periodic_job_id',)
    periodic_job_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='periodicJobId')


class PeriodicJobPagination(sgqlc.types.Type):
    __schema__ = crawlers_api_schema
    __field_names__ = ('list_periodic_job', 'total')
    list_periodic_job = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null('PeriodicJob'))), graphql_name='listPeriodicJob')
    total = sgqlc.types.Field(sgqlc.types.non_null(Long), graphql_name='total')


class Platform(sgqlc.types.Type):
    __schema__ = crawlers_api_schema
    __field_names__ = ('id',)
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='id')


class ProjectHistogram(sgqlc.types.Type):
    __schema__ = crawlers_api_schema
    __field_names__ = ('canceled_job_count', 'error_job_count', 'items_scraped_count', 'jobs_count', 'project_name', 'successful_job_count', 'with_mistakes')
    canceled_job_count = sgqlc.types.Field(Int, graphql_name='canceledJobCount')
    error_job_count = sgqlc.types.Field(Int, graphql_name='errorJobCount')
    items_scraped_count = sgqlc.types.Field(Long, graphql_name='itemsScrapedCount')
    jobs_count = sgqlc.types.Field(Int, graphql_name='jobsCount')
    project_name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='projectName')
    successful_job_count = sgqlc.types.Field(Int, graphql_name='successfulJobCount')
    with_mistakes = sgqlc.types.Field(Int, graphql_name='withMistakes')


class ProjectPagination(sgqlc.types.Type):
    __schema__ = crawlers_api_schema
    __field_names__ = ('list_project', 'total')
    list_project = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null('Project'))), graphql_name='listProject')
    total = sgqlc.types.Field(sgqlc.types.non_null(Long), graphql_name='total')


class ProjectStats(sgqlc.types.Type):
    __schema__ = crawlers_api_schema
    __field_names__ = ('canceled_job_count', 'error_job_count', 'errors_count', 'items_scraped_count', 'jobs_count', 'successful_job_count', 'with_mistakes')
    canceled_job_count = sgqlc.types.Field(Int, graphql_name='canceledJobCount')
    error_job_count = sgqlc.types.Field(Int, graphql_name='errorJobCount')
    errors_count = sgqlc.types.Field(Int, graphql_name='errorsCount')
    items_scraped_count = sgqlc.types.Field(Long, graphql_name='itemsScrapedCount')
    jobs_count = sgqlc.types.Field(Int, graphql_name='jobsCount')
    successful_job_count = sgqlc.types.Field(Int, graphql_name='successfulJobCount')
    with_mistakes = sgqlc.types.Field(Int, graphql_name='withMistakes')


class Query(sgqlc.types.Type):
    __schema__ = crawlers_api_schema
    __field_names__ = ('analytics', 'check_periodic_job_by_input', 'crawl_state', 'crawl_state_by_parameters', 'crawler', 'crawler_args_and_settings_description', 'crawler_by_information_source', 'crawler_site_map', 'credential', 'event_materializer', 'export_periodic_jobs', 'information_source', 'information_source_loader', 'job', 'list_crawler', 'list_job', 'list_version', 'pagination_crawl_state', 'pagination_crawler', 'pagination_credential', 'pagination_egg_file_versions_project', 'pagination_information_source', 'pagination_information_source_loader', 'pagination_job', 'pagination_job_logs', 'pagination_job_metrics', 'pagination_job_requests', 'pagination_periodic_job', 'pagination_periodic_job_logs', 'pagination_periodic_job_metrics', 'pagination_periodic_job_requests', 'pagination_project', 'pagination_recovery_job', 'pagination_versions_crawler', 'periodic_job', 'project', 'project_args_and_settings_description', 'project_default_args_and_settings_description', 'recovery_job', 'version')
    analytics = sgqlc.types.Field(sgqlc.types.non_null('Stats'), graphql_name='analytics')
    check_periodic_job_by_input = sgqlc.types.Field('PeriodicJob', graphql_name='checkPeriodicJobByInput', args=sgqlc.types.ArgDict((
        ('periodic_job_input', sgqlc.types.Arg(sgqlc.types.non_null(PeriodicJobInput), graphql_name='periodicJobInput', default=None)),
))
    )
    crawl_state = sgqlc.types.Field(sgqlc.types.non_null('CrawlState'), graphql_name='crawlState', args=sgqlc.types.ArgDict((
        ('crawl_id', sgqlc.types.Arg(sgqlc.types.non_null(ID), graphql_name='crawlId', default=None)),
))
    )
    crawl_state_by_parameters = sgqlc.types.Field(sgqlc.types.non_null('CrawlState'), graphql_name='crawlStateByParameters', args=sgqlc.types.ArgDict((
        ('crawl_state_parameters', sgqlc.types.Arg(sgqlc.types.non_null(CrawlStateParameters), graphql_name='crawlStateParameters', default=None)),
))
    )
    crawler = sgqlc.types.Field(sgqlc.types.non_null('Crawler'), graphql_name='crawler', args=sgqlc.types.ArgDict((
        ('id', sgqlc.types.Arg(sgqlc.types.non_null(ID), graphql_name='id', default=None)),
))
    )
    crawler_args_and_settings_description = sgqlc.types.Field(sgqlc.types.non_null(ArgsAndSettingsDescription), graphql_name='crawlerArgsAndSettingsDescription', args=sgqlc.types.ArgDict((
        ('crawler_id', sgqlc.types.Arg(sgqlc.types.non_null(ID), graphql_name='crawlerId', default=None)),
        ('version_id', sgqlc.types.Arg(ID, graphql_name='versionId', default=None)),
))
    )
    crawler_by_information_source = sgqlc.types.Field(sgqlc.types.non_null('Crawler'), graphql_name='crawlerByInformationSource', args=sgqlc.types.ArgDict((
        ('crawler_type', sgqlc.types.Arg(sgqlc.types.non_null(CrawlerType), graphql_name='crawlerType', default=None)),
        ('source', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='source', default=None)),
))
    )
    crawler_site_map = sgqlc.types.Field(sgqlc.types.non_null(JSON), graphql_name='crawlerSiteMap', args=sgqlc.types.ArgDict((
        ('crawler_id', sgqlc.types.Arg(sgqlc.types.non_null(ID), graphql_name='crawlerId', default=None)),
        ('version_id', sgqlc.types.Arg(sgqlc.types.non_null(ID), graphql_name='versionId', default=None)),
))
    )
    credential = sgqlc.types.Field(sgqlc.types.non_null('Credential'), graphql_name='credential', args=sgqlc.types.ArgDict((
        ('id', sgqlc.types.Arg(sgqlc.types.non_null(ID), graphql_name='id', default=None)),
))
    )
    event_materializer = sgqlc.types.Field(Event, graphql_name='eventMaterializer')
    export_periodic_jobs = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='exportPeriodicJobs', args=sgqlc.types.ArgDict((
        ('filter_settings', sgqlc.types.Arg(PeriodicJobFilterSettings, graphql_name='filterSettings', default={})),
        ('ids', sgqlc.types.Arg(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(ID))), graphql_name='ids', default=None)),
))
    )
    information_source = sgqlc.types.Field(sgqlc.types.non_null(InformationSource), graphql_name='informationSource', args=sgqlc.types.ArgDict((
        ('id', sgqlc.types.Arg(sgqlc.types.non_null(ID), graphql_name='id', default=None)),
))
    )
    information_source_loader = sgqlc.types.Field(sgqlc.types.non_null('InformationSourceLoader'), graphql_name='informationSourceLoader', args=sgqlc.types.ArgDict((
        ('id', sgqlc.types.Arg(sgqlc.types.non_null(ID), graphql_name='id', default=None)),
))
    )
    job = sgqlc.types.Field(sgqlc.types.non_null('Job'), graphql_name='job', args=sgqlc.types.ArgDict((
        ('id', sgqlc.types.Arg(sgqlc.types.non_null(ID), graphql_name='id', default=None)),
))
    )
    list_crawler = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of('Crawler')), graphql_name='listCrawler', args=sgqlc.types.ArgDict((
        ('ids', sgqlc.types.Arg(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(ID))), graphql_name='ids', default=None)),
))
    )
    list_job = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of('Job')), graphql_name='listJob', args=sgqlc.types.ArgDict((
        ('ids', sgqlc.types.Arg(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(ID))), graphql_name='ids', default=None)),
))
    )
    list_version = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of('Version')), graphql_name='listVersion', args=sgqlc.types.ArgDict((
        ('ids', sgqlc.types.Arg(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(ID))), graphql_name='ids', default=None)),
))
    )
    pagination_crawl_state = sgqlc.types.Field(sgqlc.types.non_null(CrawlStatePagination), graphql_name='paginationCrawlState', args=sgqlc.types.ArgDict((
        ('direction', sgqlc.types.Arg(SortDirection, graphql_name='direction', default='descending')),
        ('filter_settings', sgqlc.types.Arg(CrawlStateFilterSettings, graphql_name='filterSettings', default={})),
        ('limit', sgqlc.types.Arg(Int, graphql_name='limit', default=20)),
        ('offset', sgqlc.types.Arg(Int, graphql_name='offset', default=0)),
        ('sort_field', sgqlc.types.Arg(CrawlStateSorting, graphql_name='sortField', default='id')),
))
    )
    pagination_crawler = sgqlc.types.Field(sgqlc.types.non_null(CrawlerPagination), graphql_name='paginationCrawler', args=sgqlc.types.ArgDict((
        ('direction', sgqlc.types.Arg(SortDirection, graphql_name='direction', default='descending')),
        ('filter_settings', sgqlc.types.Arg(CrawlerFilterSettings, graphql_name='filterSettings', default={})),
        ('limit', sgqlc.types.Arg(Int, graphql_name='limit', default=20)),
        ('offset', sgqlc.types.Arg(Int, graphql_name='offset', default=0)),
        ('sort_field', sgqlc.types.Arg(CrawlerSorting, graphql_name='sortField', default='id')),
))
    )
    pagination_credential = sgqlc.types.Field(sgqlc.types.non_null(CredentialPagination), graphql_name='paginationCredential', args=sgqlc.types.ArgDict((
        ('direction', sgqlc.types.Arg(SortDirection, graphql_name='direction', default='descending')),
        ('filter_settings', sgqlc.types.Arg(sgqlc.types.non_null(CredentialFilterSettings), graphql_name='filterSettings', default=None)),
        ('limit', sgqlc.types.Arg(Int, graphql_name='limit', default=20)),
        ('offset', sgqlc.types.Arg(Int, graphql_name='offset', default=0)),
        ('sort_field', sgqlc.types.Arg(CredentialSorting, graphql_name='sortField', default='id')),
))
    )
    pagination_egg_file_versions_project = sgqlc.types.Field(sgqlc.types.non_null('VersionPagination'), graphql_name='paginationEggFileVersionsProject', args=sgqlc.types.ArgDict((
        ('direction', sgqlc.types.Arg(SortDirection, graphql_name='direction', default='descending')),
        ('id', sgqlc.types.Arg(sgqlc.types.non_null(ID), graphql_name='id', default=None)),
        ('limit', sgqlc.types.Arg(Int, graphql_name='limit', default=20)),
        ('offset', sgqlc.types.Arg(Int, graphql_name='offset', default=0)),
        ('sort_field', sgqlc.types.Arg(VersionSorting, graphql_name='sortField', default='id')),
        ('with_removed', sgqlc.types.Arg(sgqlc.types.non_null(Boolean), graphql_name='withRemoved', default=False)),
))
    )
    pagination_information_source = sgqlc.types.Field(sgqlc.types.non_null(InformationSourcePagination), graphql_name='paginationInformationSource', args=sgqlc.types.ArgDict((
        ('direction', sgqlc.types.Arg(SortDirection, graphql_name='direction', default='descending')),
        ('filter_settings', sgqlc.types.Arg(sgqlc.types.non_null(InformationSourceFilterSettings), graphql_name='filterSettings', default=None)),
        ('limit', sgqlc.types.Arg(Int, graphql_name='limit', default=20)),
        ('offset', sgqlc.types.Arg(Int, graphql_name='offset', default=0)),
        ('sort_field', sgqlc.types.Arg(InformationSourceSorting, graphql_name='sortField', default='id')),
))
    )
    pagination_information_source_loader = sgqlc.types.Field(sgqlc.types.non_null(InformationSourceLoaderPagination), graphql_name='paginationInformationSourceLoader', args=sgqlc.types.ArgDict((
        ('direction', sgqlc.types.Arg(SortDirection, graphql_name='direction', default='descending')),
        ('filter_settings', sgqlc.types.Arg(InformationSourceLoaderFilterSettings, graphql_name='filterSettings', default={})),
        ('limit', sgqlc.types.Arg(Int, graphql_name='limit', default=20)),
        ('offset', sgqlc.types.Arg(Int, graphql_name='offset', default=0)),
        ('sort_field', sgqlc.types.Arg(InformationSourceLoaderSorting, graphql_name='sortField', default='id')),
))
    )
    pagination_job = sgqlc.types.Field(sgqlc.types.non_null(JobPagination), graphql_name='paginationJob', args=sgqlc.types.ArgDict((
        ('direction', sgqlc.types.Arg(SortDirection, graphql_name='direction', default='descending')),
        ('jobs_filter_settings', sgqlc.types.Arg(JobsFilterSettings, graphql_name='jobsFilterSettings', default={})),
        ('limit', sgqlc.types.Arg(Int, graphql_name='limit', default=20)),
        ('offset', sgqlc.types.Arg(Int, graphql_name='offset', default=0)),
        ('sort_field', sgqlc.types.Arg(JobSorting, graphql_name='sortField', default='id')),
))
    )
    pagination_job_logs = sgqlc.types.Field(sgqlc.types.non_null(LogPagination), graphql_name='paginationJobLogs', args=sgqlc.types.ArgDict((
        ('direction', sgqlc.types.Arg(SortDirection, graphql_name='direction', default='descending')),
        ('filter_settings', sgqlc.types.Arg(LogFilterSettings, graphql_name='filterSettings', default={})),
        ('id', sgqlc.types.Arg(sgqlc.types.non_null(ID), graphql_name='id', default=None)),
        ('limit', sgqlc.types.Arg(Int, graphql_name='limit', default=20)),
        ('offset', sgqlc.types.Arg(Int, graphql_name='offset', default=0)),
        ('sort_field', sgqlc.types.Arg(LogSorting, graphql_name='sortField', default='timestamp')),
))
    )
    pagination_job_metrics = sgqlc.types.Field(sgqlc.types.non_null(MetricPagination), graphql_name='paginationJobMetrics', args=sgqlc.types.ArgDict((
        ('direction', sgqlc.types.Arg(SortDirection, graphql_name='direction', default='descending')),
        ('filter_settings', sgqlc.types.Arg(MetricFilterSettings, graphql_name='filterSettings', default={})),
        ('id', sgqlc.types.Arg(sgqlc.types.non_null(ID), graphql_name='id', default=None)),
        ('limit', sgqlc.types.Arg(Int, graphql_name='limit', default=20)),
        ('offset', sgqlc.types.Arg(Int, graphql_name='offset', default=0)),
        ('sort_field', sgqlc.types.Arg(MetricSorting, graphql_name='sortField', default='timestamp')),
))
    )
    pagination_job_requests = sgqlc.types.Field(sgqlc.types.non_null('RequestPagination'), graphql_name='paginationJobRequests', args=sgqlc.types.ArgDict((
        ('direction', sgqlc.types.Arg(SortDirection, graphql_name='direction', default='descending')),
        ('filter_settings', sgqlc.types.Arg(RequestFilterSettings, graphql_name='filterSettings', default={})),
        ('id', sgqlc.types.Arg(sgqlc.types.non_null(ID), graphql_name='id', default=None)),
        ('limit', sgqlc.types.Arg(Int, graphql_name='limit', default=20)),
        ('offset', sgqlc.types.Arg(Int, graphql_name='offset', default=0)),
        ('sort_field', sgqlc.types.Arg(RequestSorting, graphql_name='sortField', default='timestamp')),
))
    )
    pagination_periodic_job = sgqlc.types.Field(sgqlc.types.non_null(PeriodicJobPagination), graphql_name='paginationPeriodicJob', args=sgqlc.types.ArgDict((
        ('direction', sgqlc.types.Arg(SortDirection, graphql_name='direction', default='descending')),
        ('filter_settings', sgqlc.types.Arg(PeriodicJobFilterSettings, graphql_name='filterSettings', default={})),
        ('limit', sgqlc.types.Arg(Int, graphql_name='limit', default=20)),
        ('offset', sgqlc.types.Arg(Int, graphql_name='offset', default=0)),
        ('sort_field', sgqlc.types.Arg(PeriodicJobSorting, graphql_name='sortField', default='id')),
))
    )
    pagination_periodic_job_logs = sgqlc.types.Field(sgqlc.types.non_null(LogPagination), graphql_name='paginationPeriodicJobLogs', args=sgqlc.types.ArgDict((
        ('direction', sgqlc.types.Arg(SortDirection, graphql_name='direction', default='descending')),
        ('filter_settings', sgqlc.types.Arg(LogFilterSettings, graphql_name='filterSettings', default={})),
        ('id', sgqlc.types.Arg(sgqlc.types.non_null(ID), graphql_name='id', default=None)),
        ('limit', sgqlc.types.Arg(Int, graphql_name='limit', default=20)),
        ('offset', sgqlc.types.Arg(Int, graphql_name='offset', default=0)),
        ('sort_field', sgqlc.types.Arg(LogSorting, graphql_name='sortField', default='timestamp')),
))
    )
    pagination_periodic_job_metrics = sgqlc.types.Field(sgqlc.types.non_null(MetricPagination), graphql_name='paginationPeriodicJobMetrics', args=sgqlc.types.ArgDict((
        ('direction', sgqlc.types.Arg(SortDirection, graphql_name='direction', default='descending')),
        ('filter_settings', sgqlc.types.Arg(MetricFilterSettings, graphql_name='filterSettings', default={})),
        ('id', sgqlc.types.Arg(sgqlc.types.non_null(ID), graphql_name='id', default=None)),
        ('limit', sgqlc.types.Arg(Int, graphql_name='limit', default=20)),
        ('offset', sgqlc.types.Arg(Int, graphql_name='offset', default=0)),
        ('sort_field', sgqlc.types.Arg(MetricSorting, graphql_name='sortField', default='timestamp')),
))
    )
    pagination_periodic_job_requests = sgqlc.types.Field(sgqlc.types.non_null('RequestPagination'), graphql_name='paginationPeriodicJobRequests', args=sgqlc.types.ArgDict((
        ('direction', sgqlc.types.Arg(SortDirection, graphql_name='direction', default='descending')),
        ('filter_settings', sgqlc.types.Arg(RequestFilterSettings, graphql_name='filterSettings', default={})),
        ('id', sgqlc.types.Arg(sgqlc.types.non_null(ID), graphql_name='id', default=None)),
        ('limit', sgqlc.types.Arg(Int, graphql_name='limit', default=20)),
        ('offset', sgqlc.types.Arg(Int, graphql_name='offset', default=0)),
        ('sort_field', sgqlc.types.Arg(RequestSorting, graphql_name='sortField', default='timestamp')),
))
    )
    pagination_project = sgqlc.types.Field(sgqlc.types.non_null(ProjectPagination), graphql_name='paginationProject', args=sgqlc.types.ArgDict((
        ('direction', sgqlc.types.Arg(SortDirection, graphql_name='direction', default='descending')),
        ('filter_settings', sgqlc.types.Arg(ProjectFilterSettings, graphql_name='filterSettings', default={})),
        ('limit', sgqlc.types.Arg(Int, graphql_name='limit', default=20)),
        ('offset', sgqlc.types.Arg(Int, graphql_name='offset', default=0)),
        ('sort_field', sgqlc.types.Arg(ProjectSorting, graphql_name='sortField', default='id')),
))
    )
    pagination_recovery_job = sgqlc.types.Field(sgqlc.types.non_null('RecoveryJobPagination'), graphql_name='paginationRecoveryJob', args=sgqlc.types.ArgDict((
        ('direction', sgqlc.types.Arg(SortDirection, graphql_name='direction', default='descending')),
        ('filter_settings', sgqlc.types.Arg(RecoveryJobFilterSettings, graphql_name='filterSettings', default={})),
        ('limit', sgqlc.types.Arg(Int, graphql_name='limit', default=20)),
        ('offset', sgqlc.types.Arg(Int, graphql_name='offset', default=0)),
        ('sort_field', sgqlc.types.Arg(RecoveryJobSorting, graphql_name='sortField', default='id')),
))
    )
    pagination_versions_crawler = sgqlc.types.Field(sgqlc.types.non_null('VersionPagination'), graphql_name='paginationVersionsCrawler', args=sgqlc.types.ArgDict((
        ('direction', sgqlc.types.Arg(SortDirection, graphql_name='direction', default='descending')),
        ('filter_settings', sgqlc.types.Arg(VersionFilterSettings, graphql_name='filterSettings', default={'withRemovedVersions': False})),
        ('id', sgqlc.types.Arg(sgqlc.types.non_null(ID), graphql_name='id', default=None)),
        ('limit', sgqlc.types.Arg(Int, graphql_name='limit', default=20)),
        ('offset', sgqlc.types.Arg(Int, graphql_name='offset', default=0)),
        ('sort_field', sgqlc.types.Arg(VersionSorting, graphql_name='sortField', default='id')),
))
    )
    periodic_job = sgqlc.types.Field(sgqlc.types.non_null('PeriodicJob'), graphql_name='periodicJob', args=sgqlc.types.ArgDict((
        ('id', sgqlc.types.Arg(sgqlc.types.non_null(ID), graphql_name='id', default=None)),
))
    )
    project = sgqlc.types.Field(sgqlc.types.non_null('Project'), graphql_name='project', args=sgqlc.types.ArgDict((
        ('id', sgqlc.types.Arg(sgqlc.types.non_null(ID), graphql_name='id', default=None)),
))
    )
    project_args_and_settings_description = sgqlc.types.Field(sgqlc.types.non_null(ArgsAndSettingsDescription), graphql_name='projectArgsAndSettingsDescription', args=sgqlc.types.ArgDict((
        ('id', sgqlc.types.Arg(sgqlc.types.non_null(ID), graphql_name='id', default=None)),
        ('version_id', sgqlc.types.Arg(ID, graphql_name='versionId', default=None)),
))
    )
    project_default_args_and_settings_description = sgqlc.types.Field(sgqlc.types.non_null(ArgsAndSettingsDescription), graphql_name='projectDefaultArgsAndSettingsDescription')
    recovery_job = sgqlc.types.Field(sgqlc.types.non_null('RecoveryJob'), graphql_name='recoveryJob', args=sgqlc.types.ArgDict((
        ('id', sgqlc.types.Arg(sgqlc.types.non_null(ID), graphql_name='id', default=None)),
))
    )
    version = sgqlc.types.Field(sgqlc.types.non_null('Version'), graphql_name='version', args=sgqlc.types.ArgDict((
        ('id', sgqlc.types.Arg(sgqlc.types.non_null(ID), graphql_name='id', default=None)),
))
    )


class RecoveryJob(sgqlc.types.Type):
    __schema__ = crawlers_api_schema
    __field_names__ = ('crawler', 'creator', 'end_time', 'id', 'last_updater', 'progress', 'progress_message', 'result_version', 'source_version', 'start_time', 'status', 'system_registration_date', 'system_update_date')
    crawler = sgqlc.types.Field(sgqlc.types.non_null('Crawler'), graphql_name='crawler')
    creator = sgqlc.types.Field(sgqlc.types.non_null('User'), graphql_name='creator')
    end_time = sgqlc.types.Field(UnixTime, graphql_name='endTime')
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='id')
    last_updater = sgqlc.types.Field('User', graphql_name='lastUpdater')
    progress = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='progress')
    progress_message = sgqlc.types.Field(String, graphql_name='progressMessage')
    result_version = sgqlc.types.Field('Version', graphql_name='resultVersion')
    source_version = sgqlc.types.Field(sgqlc.types.non_null('Version'), graphql_name='sourceVersion')
    start_time = sgqlc.types.Field(UnixTime, graphql_name='startTime')
    status = sgqlc.types.Field(sgqlc.types.non_null(RecoveryJobStatus), graphql_name='status')
    system_registration_date = sgqlc.types.Field(sgqlc.types.non_null(UnixTime), graphql_name='systemRegistrationDate')
    system_update_date = sgqlc.types.Field(UnixTime, graphql_name='systemUpdateDate')


class RecoveryJobPagination(sgqlc.types.Type):
    __schema__ = crawlers_api_schema
    __field_names__ = ('list_recovery_job', 'total')
    list_recovery_job = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(RecoveryJob))), graphql_name='listRecoveryJob')
    total = sgqlc.types.Field(sgqlc.types.non_null(Long), graphql_name='total')


class Request(sgqlc.types.Type):
    __schema__ = crawlers_api_schema
    __field_names__ = ('duration', 'fingerprint', 'http_status', 'job_id', 'last_seen', 'method', 'request_url', 'response_size', 'timestamp', 'url')
    duration = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='duration')
    fingerprint = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='fingerprint')
    http_status = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='httpStatus')
    job_id = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='jobId')
    last_seen = sgqlc.types.Field(sgqlc.types.non_null(UnixTime), graphql_name='lastSeen')
    method = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='method')
    request_url = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='requestUrl')
    response_size = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='responseSize')
    timestamp = sgqlc.types.Field(sgqlc.types.non_null(UnixTime), graphql_name='timestamp')
    url = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='url')


class RequestPagination(sgqlc.types.Type):
    __schema__ = crawlers_api_schema
    __field_names__ = ('list_request', 'total')
    list_request = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(Request))), graphql_name='listRequest')
    total = sgqlc.types.Field(sgqlc.types.non_null(Long), graphql_name='total')


class SettingDescription(sgqlc.types.Type):
    __schema__ = crawlers_api_schema
    __field_names__ = ('default', 'long_description', 'name', 'required', 'short_description', 'type')
    default = sgqlc.types.Field(String, graphql_name='default')
    long_description = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='longDescription')
    name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='name')
    required = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='required')
    short_description = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='shortDescription')
    type = sgqlc.types.Field(sgqlc.types.non_null(SettingsType), graphql_name='type')


class State(sgqlc.types.Type):
    __schema__ = crawlers_api_schema
    __field_names__ = ('is_success',)
    is_success = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='isSuccess')


class Stats(sgqlc.types.Type):
    __schema__ = crawlers_api_schema
    __field_names__ = ('items_histogram', 'jobs_metrics', 'previous_items_histogram', 'projects_histogram', 'type_of_stats', 'user_id')
    items_histogram = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(DateHistogramBucket))), graphql_name='itemsHistogram', args=sgqlc.types.ArgDict((
        ('interval', sgqlc.types.Arg(TimestampInterval, graphql_name='interval', default=None)),
))
    )
    jobs_metrics = sgqlc.types.Field(sgqlc.types.non_null(JobStats), graphql_name='jobsMetrics', args=sgqlc.types.ArgDict((
        ('interval', sgqlc.types.Arg(TimestampInterval, graphql_name='interval', default=None)),
))
    )
    previous_items_histogram = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(DateHistogramBucket))), graphql_name='previousItemsHistogram', args=sgqlc.types.ArgDict((
        ('interval', sgqlc.types.Arg(TimestampInterval, graphql_name='interval', default=None)),
))
    )
    projects_histogram = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(ProjectHistogram))), graphql_name='projectsHistogram', args=sgqlc.types.ArgDict((
        ('interval', sgqlc.types.Arg(TimestampInterval, graphql_name='interval', default=None)),
))
    )
    type_of_stats = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='typeOfStats')
    user_id = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='userId')


class Subscription(sgqlc.types.Type):
    __schema__ = crawlers_api_schema
    __field_names__ = ('job',)
    job = sgqlc.types.Field(sgqlc.types.non_null(JobSubscription), graphql_name='job', args=sgqlc.types.ArgDict((
        ('direction', sgqlc.types.Arg(SortDirection, graphql_name='direction', default='descending')),
        ('jobs_filter_settings', sgqlc.types.Arg(JobsFilterSettings, graphql_name='jobsFilterSettings', default={})),
        ('limit', sgqlc.types.Arg(Int, graphql_name='limit', default=20)),
        ('offset', sgqlc.types.Arg(Int, graphql_name='offset', default=0)),
        ('sort_field', sgqlc.types.Arg(JobSorting, graphql_name='sortField', default='id')),
))
    )


class User(sgqlc.types.Type):
    __schema__ = crawlers_api_schema
    __field_names__ = ('id',)
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='id')


class VersionPagination(sgqlc.types.Type):
    __schema__ = crawlers_api_schema
    __field_names__ = ('list_version', 'total')
    list_version = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null('Version'))), graphql_name='listVersion')
    total = sgqlc.types.Field(sgqlc.types.non_null(Long), graphql_name='total')


class CrawlState(sgqlc.types.Type, RecordInterface):
    __schema__ = crawlers_api_schema
    __field_names__ = ('cookie', 'crawl_key', 'crawler_id', 'credential_id', 'id', 'information_source_id', 'periodic_job_id', 'state', 'state_version')
    cookie = sgqlc.types.Field(JSON, graphql_name='cookie')
    crawl_key = sgqlc.types.Field(String, graphql_name='crawlKey')
    crawler_id = sgqlc.types.Field(ID, graphql_name='crawlerId')
    credential_id = sgqlc.types.Field(ID, graphql_name='credentialId')
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='id')
    information_source_id = sgqlc.types.Field(ID, graphql_name='informationSourceId')
    periodic_job_id = sgqlc.types.Field(ID, graphql_name='periodicJobId')
    state = sgqlc.types.Field(sgqlc.types.non_null(JSON), graphql_name='state')
    state_version = sgqlc.types.Field(sgqlc.types.non_null(Long), graphql_name='stateVersion')


class Crawler(sgqlc.types.Type, RecordInterface):
    __schema__ = crawlers_api_schema
    __field_names__ = ('analytics', 'args', 'avg_performance_time', 'crawler_type', 'current_version', 'description', 'distribution_type', 'histogram_items', 'histogram_requests', 'id', 'job_stats', 'last_collection_date', 'name', 'onetime_jobs_num', 'periodic_jobs_num', 'project', 'settings', 'start_urls', 'title')
    analytics = sgqlc.types.Field(sgqlc.types.non_null(CrawlerStats), graphql_name='analytics', args=sgqlc.types.ArgDict((
        ('interval', sgqlc.types.Arg(TimestampInterval, graphql_name='interval', default=None)),
))
    )
    args = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(KeyValue))), graphql_name='args')
    avg_performance_time = sgqlc.types.Field(Float, graphql_name='avgPerformanceTime')
    crawler_type = sgqlc.types.Field(sgqlc.types.non_null(CrawlerType), graphql_name='crawlerType')
    current_version = sgqlc.types.Field('Version', graphql_name='currentVersion')
    description = sgqlc.types.Field(String, graphql_name='description')
    distribution_type = sgqlc.types.Field(sgqlc.types.non_null(DistributionType), graphql_name='distributionType')
    histogram_items = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(DateHistogramBucket))), graphql_name='histogramItems', args=sgqlc.types.ArgDict((
        ('interval', sgqlc.types.Arg(TimestampInterval, graphql_name='interval', default=None)),
))
    )
    histogram_requests = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(DateHistogramBucket))), graphql_name='histogramRequests', args=sgqlc.types.ArgDict((
        ('interval', sgqlc.types.Arg(TimestampInterval, graphql_name='interval', default=None)),
))
    )
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='id')
    job_stats = sgqlc.types.Field(sgqlc.types.non_null(JobStats), graphql_name='jobStats', args=sgqlc.types.ArgDict((
        ('interval', sgqlc.types.Arg(TimestampInterval, graphql_name='interval', default=None)),
))
    )
    last_collection_date = sgqlc.types.Field(UnixTime, graphql_name='lastCollectionDate')
    name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='name')
    onetime_jobs_num = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='onetimeJobsNum')
    periodic_jobs_num = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='periodicJobsNum')
    project = sgqlc.types.Field(sgqlc.types.non_null('Project'), graphql_name='project')
    settings = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(KeyValue))), graphql_name='settings')
    start_urls = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(String)), graphql_name='startUrls')
    title = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='title')


class Credential(sgqlc.types.Type, RecordInterface):
    __schema__ = crawlers_api_schema
    __field_names__ = ('data_type', 'description', 'domain', 'id', 'login', 'password', 'projects', 'status', 'token')
    data_type = sgqlc.types.Field(sgqlc.types.non_null(CredentialType), graphql_name='dataType')
    description = sgqlc.types.Field(String, graphql_name='description')
    domain = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='domain')
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='id')
    login = sgqlc.types.Field(String, graphql_name='login')
    password = sgqlc.types.Field(String, graphql_name='password')
    projects = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null('Project'))), graphql_name='projects')
    status = sgqlc.types.Field(sgqlc.types.non_null(CredentialStatus), graphql_name='status')
    token = sgqlc.types.Field(String, graphql_name='token')


class InformationSourceLoader(sgqlc.types.Type, RecordInterface):
    __schema__ = crawlers_api_schema
    __field_names__ = ('actual_status', 'id', 'is_retrospective', 'metrics', 'retrospective_end', 'retrospective_start', 'running_status', 'status', 'title')
    actual_status = sgqlc.types.Field(sgqlc.types.non_null(InformationSourceLoaderActualStatus), graphql_name='actualStatus')
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='id')
    is_retrospective = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='isRetrospective')
    metrics = sgqlc.types.Field(sgqlc.types.non_null(InformationSourceLoaderStats), graphql_name='metrics')
    retrospective_end = sgqlc.types.Field(UnixTime, graphql_name='retrospectiveEnd')
    retrospective_start = sgqlc.types.Field(UnixTime, graphql_name='retrospectiveStart')
    running_status = sgqlc.types.Field(sgqlc.types.non_null(RunningStatus), graphql_name='runningStatus')
    status = sgqlc.types.Field(sgqlc.types.non_null(CollectionStatus), graphql_name='status')
    title = sgqlc.types.Field(sgqlc.types.non_null('InformationSourceLoaderTitle'), graphql_name='title')


class Job(sgqlc.types.Type, RecordInterface):
    __schema__ = crawlers_api_schema
    __field_names__ = ('args', 'collection_status', 'crawler', 'credential', 'end_time', 'histogram_items', 'histogram_requests', 'id', 'is_noise', 'job_stats', 'message_priority', 'metrics', 'monitoring_status', 'periodic_job', 'platforms', 'priority', 'project', 'schema', 'settings', 'start_time', 'status', 'version')
    args = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(KeyValue))), graphql_name='args')
    collection_status = sgqlc.types.Field(sgqlc.types.non_null(CollectionStatus), graphql_name='collectionStatus')
    crawler = sgqlc.types.Field(sgqlc.types.non_null(Crawler), graphql_name='crawler')
    credential = sgqlc.types.Field(Credential, graphql_name='credential')
    end_time = sgqlc.types.Field(UnixTime, graphql_name='endTime')
    histogram_items = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(DateHistogramBucket))), graphql_name='histogramItems')
    histogram_requests = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(DateHistogramBucket))), graphql_name='histogramRequests')
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='id')
    is_noise = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='isNoise')
    job_stats = sgqlc.types.Field(JobStats, graphql_name='jobStats')
    message_priority = sgqlc.types.Field(sgqlc.types.non_null(MessagePriority), graphql_name='messagePriority')
    metrics = sgqlc.types.Field(JobMetrics, graphql_name='metrics')
    monitoring_status = sgqlc.types.Field(sgqlc.types.non_null(MonitoringStatus), graphql_name='monitoringStatus')
    periodic_job = sgqlc.types.Field('PeriodicJob', graphql_name='periodicJob')
    platforms = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(Platform))), graphql_name='platforms')
    priority = sgqlc.types.Field(sgqlc.types.non_null(JobPriorityType), graphql_name='priority')
    project = sgqlc.types.Field(sgqlc.types.non_null('Project'), graphql_name='project')
    schema = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(KeyValue))), graphql_name='schema')
    settings = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(KeyValue))), graphql_name='settings')
    start_time = sgqlc.types.Field(UnixTime, graphql_name='startTime')
    status = sgqlc.types.Field(sgqlc.types.non_null(JobStatus), graphql_name='status')
    version = sgqlc.types.Field(sgqlc.types.non_null('Version'), graphql_name='version')


class PeriodicJob(sgqlc.types.Type, RecordInterface):
    __schema__ = crawlers_api_schema
    __field_names__ = ('args', 'crawler', 'credential', 'cron', 'cron_utcoffset_minutes', 'description', 'disable_time', 'histogram_items', 'histogram_requests', 'id', 'job_failed_monitoring_statuses', 'job_stats', 'message_priority', 'metrics', 'monitoring_status', 'name', 'next_schedule_time', 'platforms', 'priority', 'project', 'settings', 'status', 'update_on_reload', 'version')
    args = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(KeyValue))), graphql_name='args')
    crawler = sgqlc.types.Field(sgqlc.types.non_null(Crawler), graphql_name='crawler')
    credential = sgqlc.types.Field(Credential, graphql_name='credential')
    cron = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='cron')
    cron_utcoffset_minutes = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='cronUTCOffsetMinutes')
    description = sgqlc.types.Field(String, graphql_name='description')
    disable_time = sgqlc.types.Field(UnixTime, graphql_name='disableTime')
    histogram_items = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(DateHistogramBucket))), graphql_name='histogramItems', args=sgqlc.types.ArgDict((
        ('interval', sgqlc.types.Arg(TimestampInterval, graphql_name='interval', default=None)),
))
    )
    histogram_requests = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(DateHistogramBucket))), graphql_name='histogramRequests', args=sgqlc.types.ArgDict((
        ('interval', sgqlc.types.Arg(TimestampInterval, graphql_name='interval', default=None)),
))
    )
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='id')
    job_failed_monitoring_statuses = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(MonitoringStatus))), graphql_name='jobFailedMonitoringStatuses')
    job_stats = sgqlc.types.Field(sgqlc.types.non_null(JobStats), graphql_name='jobStats', args=sgqlc.types.ArgDict((
        ('interval', sgqlc.types.Arg(TimestampInterval, graphql_name='interval', default=None)),
))
    )
    message_priority = sgqlc.types.Field(sgqlc.types.non_null(MessagePriority), graphql_name='messagePriority')
    metrics = sgqlc.types.Field(PeriodicJobMetrics, graphql_name='metrics')
    monitoring_status = sgqlc.types.Field(sgqlc.types.non_null(MonitoringStatus), graphql_name='monitoringStatus')
    name = sgqlc.types.Field(String, graphql_name='name')
    next_schedule_time = sgqlc.types.Field(UnixTime, graphql_name='nextScheduleTime')
    platforms = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(Platform))), graphql_name='platforms')
    priority = sgqlc.types.Field(sgqlc.types.non_null(JobPriorityType), graphql_name='priority')
    project = sgqlc.types.Field(sgqlc.types.non_null('Project'), graphql_name='project')
    settings = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(KeyValue))), graphql_name='settings')
    status = sgqlc.types.Field(sgqlc.types.non_null(RunningStatus), graphql_name='status')
    update_on_reload = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='updateOnReload')
    version = sgqlc.types.Field(sgqlc.types.non_null('Version'), graphql_name='version')


class Project(sgqlc.types.Type, RecordInterface):
    __schema__ = crawlers_api_schema
    __field_names__ = ('args', 'crawlers_num', 'current_version', 'description', 'egg_file', 'histogram_crawlers', 'histogram_items', 'id', 'jobs_num', 'name', 'periodic_jobs_num', 'project_stats', 'settings', 'title')
    args = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(KeyValue))), graphql_name='args')
    crawlers_num = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='crawlersNum')
    current_version = sgqlc.types.Field('Version', graphql_name='currentVersion')
    description = sgqlc.types.Field(String, graphql_name='description')
    egg_file = sgqlc.types.Field(String, graphql_name='eggFile')
    histogram_crawlers = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(CrawlerHistogram))), graphql_name='histogramCrawlers', args=sgqlc.types.ArgDict((
        ('interval', sgqlc.types.Arg(TimestampInterval, graphql_name='interval', default=None)),
))
    )
    histogram_items = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(DateHistogramBucket))), graphql_name='histogramItems', args=sgqlc.types.ArgDict((
        ('interval', sgqlc.types.Arg(TimestampInterval, graphql_name='interval', default=None)),
))
    )
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='id')
    jobs_num = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='jobsNum')
    name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='name')
    periodic_jobs_num = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='periodicJobsNum')
    project_stats = sgqlc.types.Field(sgqlc.types.non_null(ProjectStats), graphql_name='projectStats', args=sgqlc.types.ArgDict((
        ('interval', sgqlc.types.Arg(TimestampInterval, graphql_name='interval', default=None)),
))
    )
    settings = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(KeyValue))), graphql_name='settings')
    title = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='title')


class Version(sgqlc.types.Type, RecordInterface):
    __schema__ = crawlers_api_schema
    __field_names__ = ('deploy_status', 'id', 'project_id', 'status', 'version_name')
    deploy_status = sgqlc.types.Field(sgqlc.types.non_null(DeployStatus), graphql_name='deployStatus')
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='id')
    project_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='projectId')
    status = sgqlc.types.Field(sgqlc.types.non_null(VersionStatus), graphql_name='status')
    version_name = sgqlc.types.Field(sgqlc.types.non_null(Long), graphql_name='versionName')



########################################################################
# Unions
########################################################################
class InformationSourceLoaderTitle(sgqlc.types.Union):
    __schema__ = crawlers_api_schema
    __types__ = (InformationSourceLoaderFileTitle, InformationSourceLoaderURLTitle)



########################################################################
# Schema Entry Points
########################################################################
crawlers_api_schema.query_type = Query
crawlers_api_schema.mutation_type = Mutation
crawlers_api_schema.subscription_type = Subscription

