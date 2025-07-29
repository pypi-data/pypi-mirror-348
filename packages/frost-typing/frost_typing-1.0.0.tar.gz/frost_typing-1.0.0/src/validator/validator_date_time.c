#include "field.h"
#include "validator/validator.h"

#include "datetime.h"

#define _CHAR_IS_INT(c) (ch >= '0' && ch <= '9')
#define _CHAR_TO_INT(c) ((int)(c - '0'))
#define PyTime_FromTimeAndTZ(hour, minute, second, usecond, tz)                \
    PyDateTimeAPI->Time_FromTime(                                              \
      hour, minute, second, usecond, tz, PyDateTimeAPI->TimeType)

#define PyDateTime_FromDateAndTimeAndTZ(                                       \
  year, month, day, hour, min, sec, usec, tz)                                  \
    PyDateTimeAPI->DateTime_FromDateAndTime(                                   \
      year, month, day, hour, min, sec, usec, tz, PyDateTimeAPI->DateTimeType)

#define _CACHE_SIZE 48
static PyObject* tz_cache[_CACHE_SIZE] = { NULL };
// static const int DAYS_IN_MONTH[2][13] = {
//     { 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31, 31 },
//     { 31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31, 31 }
// };

const int SECONDS_PER_DAY = 86400;
const int SECONDS_PER_HOUR = 3600;
const int SECONDS_PER_MINUTE = 60;

TypeAdapter *TypeAdapterTime, *TypeAdapterDate, *TypeAdapterDateTime;

static inline int
is_leap_year(int year)
{
    return (year % 4 == 0 && year % 100 != 0) || (year % 400 == 0);
}

static inline int
days_in_month(int month, int year)
{
    if (month == 1) {
        return is_leap_year(year) ? 29 : 28;
    }
    return month & 1 ? 30 : 31;
}

static void
timestamp_to_time_double(double timestamp, int* restrict time)
{
    int64_t seconds = (int64_t)timestamp;
    double frac = timestamp - (double)seconds;

    int64_t seconds_in_day = seconds % SECONDS_PER_DAY;
    if (seconds_in_day < 0) {
        seconds_in_day += SECONDS_PER_DAY;
    }

    time[0] = (int)(seconds_in_day / SECONDS_PER_HOUR);
    seconds_in_day %= SECONDS_PER_HOUR;
    time[1] = (int)(seconds_in_day / SECONDS_PER_MINUTE);
    time[2] = (int)(seconds_in_day % SECONDS_PER_MINUTE);
    time[3] = (int)(frac * 1e6 + 0.5);
}

static double
timestamp_to_date_dobule(double timestamp, int* restrict date)
{
    int64_t ts = (int64_t)timestamp;
    int64_t seconds_in_day = ts % SECONDS_PER_DAY;
    int64_t days = ts / SECONDS_PER_DAY;

    int year = 1970;
    while (1) {
        int y_days = is_leap_year(year) ? 366 : 365;
        if (days >= y_days) {
            days -= y_days;
            year += 1;
        } else {
            break;
        }
    }

    int d, month = 0;
    while (days >= (d = days_in_month(month, year))) {
        days -= d;
        month++;
    }

    date[0] = year;
    date[1] = month + 1;
    date[2] = (int)days + 1;
    return (double)seconds_in_day + (timestamp - (double)ts);
}

static PyObject*
timestamp_to_date(double timestamp)
{
    if (timestamp < 0.0 || !isfinite(timestamp)) {
        return NULL;
    }

    int date[3] = { 0 };
    if (timestamp_to_date_dobule(timestamp, date) != 0.0) {
        return NULL;
    }
    return PyDate_FromDate(date[0], date[1], date[2]);
}

static PyObject*
timestamp_to_time(double timestamp)
{
    if (timestamp < 0.0 || timestamp >= 86400.0 || !isfinite(timestamp)) {
        return NULL;
    }

    int time[4] = { 0 };
    timestamp_to_time_double(timestamp, time);
    return PyTime_FromTimeAndTZ(
      time[0], time[1], time[2], time[3], PyDateTimeAPI->TimeZone_UTC);
}

static PyObject*
timestamp_to_datetime(double timestamp)
{
    if (timestamp < 0.0) {
        return NULL;
    }

    int dt[7] = { 0 };
    timestamp = timestamp_to_date_dobule(timestamp, dt);
    timestamp_to_time_double(timestamp, dt + 3);
    return PyDateTime_FromDateAndTimeAndTZ(dt[0],
                                           dt[1],
                                           dt[2],
                                           dt[3],
                                           dt[4],
                                           dt[5],
                                           dt[6],
                                           PyDateTimeAPI->TimeZone_UTC);
}

PyObject*
creat_tz_info(int sign, int hout, int minute)
{
    PyObject *tz_info, *delta, *tz_name;
    int tz_minute = sign * (hout * 60 + minute);
    if (tz_minute == 0) {
        return Py_NewRef(PyDateTimeAPI->TimeZone_UTC);
    }

    int is_cache = (tz_minute + 720) % 30 == 0;
    if (is_cache) {
        tz_info = tz_cache[(tz_minute + 720) / 30];
        if (tz_info != NULL) {
            return Py_NewRef(tz_info);
        }
    }

    delta = PyDelta_FromDSU(0, tz_minute * 60, 0);
    if (delta == NULL) {
        return NULL;
    }

    tz_name = PyUnicode_FromFormat(
      "UTC%c%02u:%02u", sign == -1 ? '-' : '+', hout, minute);
    if (tz_name == NULL) {
        return NULL;
    }
    tz_info = PyTimeZone_FromOffsetAndName(delta, tz_name);
    Py_DECREF(tz_name);
    Py_DECREF(delta);
    if (is_cache) {
        tz_cache[(tz_minute + 720) / 30] = Py_NewRef(tz_info);
    }
    return tz_info;
}

static void
week_to_date(int* restrict date)
{
    int year = date[0], week = date[1], day = date[2];
    int first_day_of_year = (1 + 5 * ((year - 1) % 4) + 4 * ((year - 1) % 100) +
                             6 * ((year - 1) % 400)) %
                            7;
    int offset = (first_day_of_year == 0) ? 6 : (first_day_of_year - 1);
    int days_passed = (week - 1) * 7 + (day - 1) - offset;
    if (days_passed < 0) {
        year--;
        days_passed += is_leap_year(year) ? 366 : 365;
    }

    int d, month = 1;
    while (days_passed >= (d = days_in_month(month, year))) {
        days_passed -= d;
        month++;
    }
    date[0] = year;
    date[1] = month;
    date[2] = days_passed;
}

static Py_ssize_t
get_buffer(PyObject* obj, char** buf)
{
    PyTypeObject* tp = Py_TYPE(obj);
    if (tp == &PyUnicode_Type) {
        int kind = PyUnicode_KIND(obj);
        void* d = PyUnicode_DATA(obj);
        Py_ssize_t length = PyUnicode_GET_LENGTH(obj);
        if (kind == 1) {
            *buf = d;
            return length;
        }
        PyErr_Format(PyExc_ValueError, "Invalid isoformat string '%s'", d);
        return -1;
    }
    if (tp == &PyBytes_Type) {
        *buf = _CAST(PyBytesObject*, obj)->ob_sval;
        return PyBytes_GET_SIZE(obj);
    }
    if (tp == &PyByteArray_Type) {
        *buf = _CAST(PyByteArrayObject*, obj)->ob_bytes;
        return PyByteArray_GET_SIZE(obj);
    }

    PyErr_Format(PyExc_TypeError,
                 "Argument must be string, or a"
                 " bytes-like object, not '%s'",
                 tp->tp_name);
    return -1;
}

static int
parse_date(const char* restrict buf,
           int length,
           int* restrict res,
           int* restrict last_ind)
{
    int st_section = 0, section_i = 0, w = 0;

    for (int ind = 0; ind < length; ++ind) {
        unsigned char ch = (unsigned char)buf[ind];
        if (ch >= '0' && ch <= '9') {
            if (section_i == 0) {
                if (ind - st_section == 4) {
                    st_section = ind;
                    ++section_i;
                }
            } else if (section_i == 1) {
                if (ind - st_section == 2) {
                    st_section = ind;
                    ++section_i;
                }
            }
            res[section_i] = res[section_i] * 10 + (ch - '0');
            continue;
        }
        if (ch == 'W' && !w) {
            if (section_i <= 1) {
                st_section = ind + 1;
                w = 1;
                section_i = 1;
                continue;
            }
        }

        if ((section_i == 0 && ind > 4) ||
            (section_i == 1 && ind - st_section > (3 + w))) {
            if (*last_ind) {
                *last_ind = ind;
                if (w) {
                    week_to_date(res);
                }
                return 0;
            }
            return -1;
        }

        if (res[section_i] == 0) {
            return -1;
        }

        st_section = ind + 1;
        if (ch != '-' || buf[ind - 1] == '-' || ++section_i > 2) {
            if (*last_ind) {
                *last_ind = ind;
                if (w) {
                    if (section_i == 1 && !res[2]) {
                        res[2] = 1;
                    }
                    week_to_date(res);
                }
                return 0;
            }
            return -1;
        }
    }

    if (buf[length - 1] == '-') {
        return -1;
    }

    if (section_i == 1) {
        res[++section_i] = 1;
    }

    if (w) {
        week_to_date(res);
    }

    return 0;
}

static int
pow_degree(int degree)
{
    switch (degree) {
        case 0:
        case 6:
            return 1;
        case 1:
            return 10;
        case 2:
            return 100;
        case 3:
            return 1000;
        case 4:
            return 10000;
        case 5:
            return 100000;
        default:
            return -1;
    }
}

static int
parse_time(const char* restrict buf,
           int length,
           int* restrict res,
           int* restrict sign)
{
    int digit, st_section = 0, section_i = 0;

    for (int ind = 0; ind < length; ++ind) {
        char ch = buf[ind];

        if (ch >= '0' && ch <= '9') {
            if (section_i < 3 || section_i == 4) {
                if (ind - st_section == 2) {
                    section_i++;
                    st_section = ind;
                }
            }
            res[section_i] = res[section_i] * 10 + (ch - '0');
            continue;
        }

        if (st_section == ind) {
            return -1;
        }

        switch (ch) {
            case 'Z':
            case 'z':
                if (section_i < 1 || *sign) {
                    return -1;
                }
                if (ind + 1 != length) {
                    return -1;
                }
                digit = pow_degree(6 - (ind - st_section));
                if (digit < 0) {
                    return -1;
                }
                res[3] *= digit;
                *sign = 1;
                return 0;
            case '-':
            case '+':
                if (section_i < 1 || *sign) {
                    return -1;
                }
                *sign = (ch == '+') ? 1 : -1;
                digit = pow_degree(6 - (ind - st_section));
                if (digit < 0) {
                    return -1;
                }
                res[3] *= digit;
                st_section = ind + 1;
                section_i = 4;
                break;

            case ':':
                if (section_i > 1 && section_i < 4) {
                    return -1;
                }
                st_section = ind + 1;
                if (++section_i == 6) {
                    return -1;
                }
                break;

            case '.':
            case ',':
                if (section_i != 2) {
                    return -1;
                }
                st_section = ind + 1;
                if (++section_i == 6) {
                    return -1;
                }
                break;

            default:
                return -1;
        }
    }

    if (!(*sign) && section_i == 3) {
        digit = pow_degree(6 - (length - st_section));
        if (digit < 0) {
            return -1;
        }
        res[3] *= digit;
    }

    return 0;
}

PyObject*
DateTiem_ParseDate(PyObject* obj)
{
    char* buf;
    Py_ssize_t length = get_buffer(obj, &buf);
    if (length == -1) {
        return NULL;
    }

    int writer[3] = { 0 };
    int last_ind = 0;
    if (length > 10 || length < 5 ||
        parse_date(buf, (int)length, writer, &last_ind) < 0) {
        goto error;
    }

    PyObject* res = PyDate_FromDate(writer[0], writer[1], writer[2]);
    if (res) {
        return res;
    }

error:
    return PyErr_Format(PyExc_ValueError, "Invalid isoformat string '%s'", buf);
}

static PyObject*
date_tiem_parse_time(PyObject* obj)
{
    char* buf;
    Py_ssize_t length = get_buffer(obj, &buf);
    if (length == -1) {
        return NULL;
    }

    int sign = 0;
    int writer[6] = { 0 };
    PyObject *tz_info, *time;
    if (length < 3 || length > 21 ||
        parse_time(buf, (int)length, writer, &sign) < 0) {
        goto error;
    }

    if (sign) {
        tz_info = creat_tz_info(sign, writer[4], writer[5]);
        if (!tz_info) {
            return NULL;
        }
    } else {
        tz_info = Py_NewRef(Py_None);
    }
    time =
      PyTime_FromTimeAndTZ(writer[0], writer[1], writer[2], writer[3], tz_info);
    Py_DECREF(tz_info);
    if (time) {
        return time;
    }

error:
    return PyErr_Format(PyExc_ValueError, "Invalid isoformat string '%s'", buf);
}

PyObject*
DateTiem_ParseTime(PyObject* obj)
{
    return date_tiem_parse_time(obj);
}

static PyObject*
date_tiem_parse_date_time(PyObject* obj)
{
    char* buf;
    Py_ssize_t length = get_buffer(obj, &buf);
    if (length == -1) {
        return NULL;
    }

    if (length < 5 || length > 32) {
        goto error;
    }

    int last_ind = -1;
    int date[3] = { 0 };
    if (parse_date(buf, (int)length, date, &last_ind) < 0) {
        goto error;
    }

    if (last_ind == -1 || last_ind == length) {
        PyObject* res =
          PyDateTime_FromDateAndTime(date[0], date[1], date[2], 0, 0, 0, 0);
        if (res) {
            return res;
        }
        goto error;
    }

    char ch = buf[last_ind++];
    if ((ch != ' ' && ch != 'T') || last_ind == length) {
        goto error;
    }

    int sign = 0;
    int time[6] = { 0 };
    length -= last_ind;
    if (parse_time(buf + last_ind, (int)length, time, &sign) < 0) {
        goto error;
    }

    PyObject* tz_info = sign ? creat_tz_info(sign, time[4], time[5]) : Py_None;
    if (!tz_info) {
        return NULL;
    }

    PyObject* dt = PyDateTime_FromDateAndTimeAndTZ(
      date[0], date[1], date[2], time[0], time[1], time[2], time[3], tz_info);

    if (sign) {
        Py_DECREF(tz_info);
    }

    if (dt) {
        return dt;
    }

error:
    return PyErr_Format(PyExc_ValueError, "Invalid isoformat string '%s'", buf);
}

PyObject*
DateTiem_ParseDateTime(PyObject* obj)
{
    return date_tiem_parse_date_time(obj);
}

static PyObject*
converter_time(TypeAdapter* self, ValidateContext* ctx, PyObject* val)
{
    if (ctx->flags & FIELD_STRICT) {
        return NULL;
    }

    if (PyLong_Check(val) && !PyBool_Check(val)) {
        return timestamp_to_time(PyLong_AsDouble(val));
    }

    if (PyFloat_Check(val)) {
        return timestamp_to_time(PyFloat_AS_DOUBLE(val));
    }
    return DateTiem_ParseTime(val);
}

static PyObject*
converter_date(TypeAdapter* self, ValidateContext* ctx, PyObject* val)
{
    if (ctx->flags & FIELD_STRICT) {
        return NULL;
    }

    if (PyLong_Check(val) && !PyBool_Check(val)) {
        return timestamp_to_date(PyLong_AsDouble(val));
    }

    if (PyFloat_Check(val)) {
        return timestamp_to_date(PyFloat_AS_DOUBLE(val));
    }
    return DateTiem_ParseDate(val);
}

static PyObject*
converter_datetime(TypeAdapter* self, ValidateContext* ctx, PyObject* val)
{
    if (ctx->flags & FIELD_STRICT) {
        return NULL;
    }

    if (PyLong_Check(val) && !PyBool_Check(val)) {
        return timestamp_to_datetime(PyLong_AsDouble(val));
    }

    if (PyFloat_Check(val)) {
        return timestamp_to_datetime(PyFloat_AS_DOUBLE(val));
    }

    return DateTiem_ParseDateTime(val);
}

inline int
DateTime_Is_DateType(PyTypeObject* tp)
{
    return tp == PyDateTimeAPI->DateType;
}

inline int
DateTime_Is_TimeType(PyTypeObject* tp)
{
    return tp == PyDateTimeAPI->TimeType;
}

inline int
DateTime_Is_DateTimeType(PyTypeObject* tp)
{
    return tp == PyDateTimeAPI->DateTimeType;
}

int
date_time_setup(void)
{
    PyDateTime_IMPORT;
    if (!PyDateTimeAPI) {
        return -1;
    }

#define TYPEADAPTER_CREATE_DT(name, h, conv, ins)                              \
    name = TypeAdapter_Create(                                                 \
      (PyObject*)h, NULL, NULL, TypeAdapter_Base_Repr, conv, ins);             \
    if (!name) {                                                               \
        return -1;                                                             \
    }

    TYPEADAPTER_CREATE_DT(TypeAdapterTime,
                          PyDateTimeAPI->TimeType,
                          converter_time,
                          Inspector_IsType);

    TYPEADAPTER_CREATE_DT(TypeAdapterDate,
                          PyDateTimeAPI->DateType,
                          converter_date,
                          Inspector_IsType);

    TYPEADAPTER_CREATE_DT(TypeAdapterDateTime,
                          PyDateTimeAPI->DateTimeType,
                          converter_datetime,
                          Inspector_IsType);
#undef TYPEADAPTER_CREATE_DT
    return 0;
}

void
date_time_free(void)
{
    Py_DECREF(TypeAdapterTime);
    Py_DECREF(TypeAdapterDate);
    Py_DECREF(TypeAdapterDateTime);

    for (Py_ssize_t i = 0; i < _CACHE_SIZE; i++) {
        Py_XDECREF(tz_cache[i]);
    }
}