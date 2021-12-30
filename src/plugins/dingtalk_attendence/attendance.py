from nonebot import logger
from datetime import datetime
from src.dingtalk_services.vacation import get_vacation
from src.dingtalk_services.absence import get_absence


async def attendance_result(query_time: datetime = datetime.now()) -> tuple[str, str]:
    """
    发送集训队的考勤状况
    :return: 缺勤和请假的信息
    """

    absence = await get_absence(query_time)

    # 请假
    in_vacation = await get_vacation(absence, query_time)
    logger.warning(f'{len(absence)} people are absent')
    # 缺勤
    bad_guys = [x for x in absence
                if x not in in_vacation]

    absence_msg = query_time.strftime("%Y年%m月%d日")
    if len(bad_guys) == 0:
        absence_msg += "全员出勤"
    else:
        absence_msg += "未出勤的有:\n"
        for i in range(len(bad_guys)):
            absence_msg += bad_guys[i][0] + '\t'
            if (i + 1) % 3 == 0:
                absence_msg += '\n'

    vacation_msg = query_time.strftime("%Y年%m月%d日")
    if len(in_vacation) == 0:
        vacation_msg += "无人请假"
    else:
        vacation_msg += "请假的人有:\n"
        for i in range(len(in_vacation)):
            vacation_msg += in_vacation[i][0] + '\t'
            if (i + 1) % 3 == 0:
                vacation_msg += '\n'

    return absence_msg, vacation_msg
