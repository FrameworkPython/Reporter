import asyncio
import rubpy
from rubpy.enums import ReportType

def input_decorator(func):
    def wrapper(*args, **kwargs):
        return func(input(*args, **kwargs))
    return wrapper

@input_decorator
def get_input(prompt):
    return prompt

def get_report_types():
    report_types = ['VIOLENCE', 'SPAM', 'PORNOGRAPHY', 'CHILD_ABUSE', 'COPYRIGHT', 'FISHING', 'OTHER']
    for i, report_type in enumerate(report_types, start=1):
        print(f"{i}. {report_type}")
    selected_types = get_input("لطفا نوع گزارش‌ها را از لیست زیر انتخاب کنید (با انتخاب اعداد مربوطه و جدا کردن آن‌ها با کاما): ")
    selected_types = selected_types.split(',')
    return [report_types[int(choice) - 1] for choice in selected_types]

async def report_multiple_times(bot, object_guid, report_types, description, times, delay):
    for report_type_str in report_types:
        report_type = ReportType[report_type_str]
        for _ in range(times):
            try:
                result = await bot.report_object(object_guid, report_type, description)
                print(result)
                print("گزارش شد")
                await asyncio.sleep(delay)
            except Exception as e:
                print(f"مشکلی در ارسال گزارش به وجود آمد: {str(e)}")

async def main():
    async with rubpy.Client(name='rubpy') as bot:
        object_guid = get_input("لطفا guid مکان را وارد کنید: ")
        report_types = get_report_types()
        description = None
        if 'OTHER' in report_types:
            description = get_input("لطفا توضیحات اضافی برای گزارش را وارد کنید: ")
        times = int(get_input("لطفا تعداد گزارش‌ها را وارد کنید: "))
        delay = int(get_input("لطفا تاخیر بین گزارش‌ها (به ثانیه) را وارد کنید: "))
        await report_multiple_times(bot, object_guid, report_types, description, times, delay)

asyncio.run(main())
