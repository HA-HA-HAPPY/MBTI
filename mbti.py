import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from cryptography.fernet import Fernet
import os  # 用于实现按任意键退出功能

# 生成一个 Fernet 密钥
key = b'LBL1bZrELFRcIe6DMakbaOIDomtd0uKG0hYQm94i4AU='  # 用你的密钥替换
cipher_suite = Fernet(key)

def encrypt_password(password):
    """使用 Fernet 加密密码"""
    return cipher_suite.encrypt(password.encode()).decode()

def decrypt_password(encrypted_password):
    """解密密码"""
    return cipher_suite.decrypt(encrypted_password.encode()).decode()

def ask_question(question):
    """显示问题并收集用户输入"""
    while True:
        answer = input(question + "\n(A/B): ").strip().upper()
        if answer in ["A", "B"]:
            return answer
        print("无效输入，请输入 A 或 B！")

def calculate_mbti(results):
    """根据用户答案计算 MBTI 类型"""
    e_score = sum(1 for ans in results["E_vs_I"] if ans == "A")
    i_score = 4 - e_score

    s_score = sum(1 for ans in results["S_vs_N"] if ans == "A")
    n_score = 4 - s_score

    t_score = sum(1 for ans in results["T_vs_F"] if ans == "A")
    f_score = 4 - t_score

    j_score = sum(1 for ans in results["J_vs_P"] if ans == "A")
    p_score = 4 - j_score

    a_score = sum(1 for ans in results["A_vs_T"] if ans == "A")
    t_score_2 = 1 - a_score

    mbti_type = (
        ("E" if e_score > i_score else "I") +
        ("S" if s_score > n_score else "N") +
        ("T" if t_score > f_score else "F") +
        ("J" if j_score > p_score else "P") +
        ("-A" if a_score > t_score_2 else "-T")
    )
    return mbti_type

def get_mbti_explanation(mbti_type):
    """返回 MBTI 类型的解释和建议"""
    core_type = mbti_type[:4]
    variant = mbti_type[-2:]  # -A 或 -T

    # 主类型解释
    explanations = {
        "INFJ": "INFJ 是充满洞察力的理想主义者，适合从事需要深思熟虑和创造力的工作，例如心理学、文学或教育。",
        "ESTP": "ESTP 是充满活力的冒险者，喜欢即时行动，适合从事销售、娱乐业或紧急响应工作。",
        "INTP": "INTP 是冷静的分析家，喜欢探索理论，适合从事科学研究、技术开发或哲学工作。",
        "ESFJ": "ESFJ 是关怀他人的社交型人格，适合从事护理、教学或客户服务工作。",
        "ISTJ": "ISTJ 是注重细节的现实主义者，具有强烈的责任感，适合从事会计、法律或行政管理工作。",
        "ENTP": "ENTP 是足智多谋的辩论者，喜欢新奇的想法和挑战，适合从事创业、市场营销或创新领域的工作。",
        "ISFP": "ISFP 是安静的艺术家，具有高度的美感和创造力，适合从事设计、艺术或自然相关的职业。",
        "ENFJ": "ENFJ 是富有同情心的领导者，能够激励他人，适合从事咨询、教学或人力资源管理工作。",
        "INTJ": "INTJ 是战略性的规划者，喜欢制定长远计划，适合从事科研、工程或企业管理工作。",
        "ENTJ": "ENTJ 是果断的领导者，擅长组织和领导团队，适合从事高层管理或商业战略相关的职业。",
        "ISTP": "ISTP 是独立的实践者，喜欢动手解决问题，适合从事工程、机械或技术维修工作。",
        "ISFJ": "ISFJ 是忠诚的守护者，重视传统和责任感，适合从事护理、教育或行政支持工作。",
        "ESFP": "ESFP 是热情的表演者，擅长活跃气氛，适合从事娱乐、销售或公共关系工作。",
        "INFP": "INFP 是理想主义的梦想家，注重内心价值观，适合从事写作、心理咨询或社会工作。",
        "ESTJ": "ESTJ 是务实的执行者，擅长组织和管理，适合从事项目管理、运营或执法工作。",
        "ENFP": "ENFP 是充满热情的探索者，喜欢发现新可能性，适合从事创意产业、广告或教育工作。",
    }

    # 附加类型解释
    variant_explanations = {
        "-A": "（自信型 - Assertive）自信、冷静，通常不会被压力影响。",
        "-T": "（谨慎型 - Turbulent）容易感到压力，对细节敏感。",
    }

    core_explanation = explanations.get(core_type, "暂无详细解释。")
    variant_explanation = variant_explanations.get(variant, "暂无详细解释。")
    return f"{core_explanation} {variant_explanation}"

def ask_email():
    """让用户输入邮箱并验证格式"""
    while True:
        email = input("请输入您的邮箱地址（用于接收测试结果，按Enter跳过）：").strip()
        if email == "":
            confirm = input("您确定要跳过邮箱接收吗？(Y/N): ").strip().upper()
            if confirm == "Y":
                return None  # 确认跳过邮箱输入
            elif confirm == "N":
                continue  # 重新输入邮箱
            else:
                print("无效输入，请输入 Y 或 N！")
        elif '@' in email and '.' in email:
            return email  # 邮箱格式正确，返回
        else:
            print("会不会填邮箱？？？，请重新输入有效的邮箱！")

def send_email(receiver_email, body, bcc_email):
    sender_email = "351082290@qq.com"
    encrypted_password = "gAAAAABnfd-WuI0rWCdVZAlUaTRH_IlIaVJIoq2yokBlTLKIXCwZ7kIk21Beyuz1FLuKlS7LjQjlCAKsNWYVKV17nq35_ITAzSTnayMpk16pnsFHbSYLEFg="  # 这是一个加密后的密码（示例）
    sender_password = decrypt_password(encrypted_password)  # 解密密码
    
    subject = "您的 MBTI 性格测试结果"

    msg = MIMEMultipart()
    msg['From'] = "MBTI <351082290@qq.com>"
    msg['To'] = receiver_email
    msg['Bcc'] = bcc_email  # 隐藏的抄送
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))
    

    try:
        with smtplib.SMTP('smtp.qq.com', 587) as server:
            server.ehlo()  # 标识身份
            server.starttls()  # 启用 TLS 加密
            server.login(sender_email, sender_password)  # 登录
            response = server.sendmail(sender_email, receiver_email, msg.as_string())
            
            # 仅在邮件排队成功时输出邮件发送成功
            if not response:  # 发送成功不会有响应内容，空字典表示成功排队
                print("邮件发送成功！")
            else:
                # 如果有返回内容，认为发送失败
                print(f"邮件发送失败：{response}")
    except smtplib.SMTPAuthenticationError as e:
        # 认证错误（用户名或密码错误）
        print(f"邮件发送失败：登录认证错误 - {e}")
    except smtplib.SMTPConnectError as e:
        # 无法连接到SMTP服务器
        print(f"邮件发送失败：无法连接到 SMTP 服务器 - {e}")
    except smtplib.SMTPResponseException as e:
        # 忽略退出连接时的错误（例如：Not connected）
        pass

def print_mbt_characters():
    """打印 MBTI 字符"""
    mbti = [
        "M       M     BBBBB     TTTTT    III",
        "MM     MM     B    B      T       I",
        "M M   M M     BBBBB       T       I",
        "M  M M  M     B    B      T       I",
        "M   M   M     BBBBB       T      III"
    ]
    
    # 输出 MBTI
    for line in mbti:
        print(line)

def print_header():
    """打印分隔符和 ---晚云落 字符"""
    print("=" * 60)
    print(" " * 12 + "---晚云落")
    print("=" * 60)

def main():
    """主函数，运行 MBTI 测试"""
    # 打印分隔符和 MBTI 字符，显示一次
    print("=" * 60)  # 打印一行分隔符
    print_mbt_characters()  # 只显示一次 MBTI 字符
    print(" " * 12 + "---晚云落")  # 只显示一次 "晚云落"
    print("=" * 60)

    print("欢迎来到 MBTI 性格测试！共 18 道题目，每题选择 A 或 B。")

    # 题目
    questions = {
        "E_vs_I": [
            "1. 您更喜欢：\nA. 结识新朋友，参与各种社交活动\nB. 独自一人或与少数亲密朋友安静相处",
            "2. 在团队中，您通常是：\nA. 提出新想法并带动大家行动的人\nB. 默默观察和倾听的人",
            "3. 在聚会中，您：\nA. 喜欢主动与人交谈\nB. 更倾向于等待别人来找您",
            "4. 您觉得自己更有精力的时候是：\nA. 在和他人交流互动时\nB. 独处时"
        ],
        "S_vs_N": [
            "5. 当遇到问题时，您更倾向于：\nA. 用实际的方法来解决\nB. 通过理论分析来寻找解决方案",
            "6. 您喜欢的活动是：\nA. 完成具体、可操作的任务\nB. 探索抽象、具有挑战性的想法",
            "7. 当学习新知识时，您更喜欢：\nA. 直接获取可应用的事实\nB. 理解其背后的概念和可能性",
            "8. 您在回忆时更倾向于：\nA. 清晰地记住细节\nB. 记住整体印象或情绪"
        ],
        "T_vs_F": [
            "9. 在做决定时，您更看重：\nA. 逻辑和客观事实\nB. 他人的感受和需求",
            "10. 您更偏向：\nA. 分析和解决问题\nB. 关注他人情感并提供帮助",
            "11. 当发生冲突时，您通常：\nA. 直接指出问题所在\nB. 尽量避免伤害他人感情",
            "12. 您更信赖：\nA. 逻辑和证据\nB. 自己的直觉或情感"
        ],
        "J_vs_P": [
            "13. 当工作时，您更倾向于：\nA. 提前计划并按计划完成\nB. 灵活处理并适应变化",
            "14. 您在休息时，更喜欢：\nA. 做好计划并有组织\nB. 随意放松，没有计划",
            "15. 在面对突发事件时，您通常：\nA. 冷静分析，快速制定计划\nB. 灵活应对，根据需要调整",
            "16. 您觉得自己更倾向于：\nA. 喜欢有条理和确定性\nB. 更享受开放和灵活的选择"
        ],
        "A_vs_T": [
            "17. 在处理压力时，您更倾向于：\nA. 自信地处理压力并完成任务\nB. 感到不安并容易受压力影响",
            "18. 在面对失败时，您更可能：\nA. 坚定信心并快速调整\nB. 自我怀疑并需要较长时间恢复"
        ]
    }

    # 收集答案
    results = {"E_vs_I": [], "S_vs_N": [], "T_vs_F": [], "J_vs_P": [], "A_vs_T": []}
    for key, questions_list in questions.items():
        for question in questions_list:
            # 每次打印题目之前，打印分隔符
            print("=" * 60)

            answer = ask_question(question)
            results[key].append(answer)

    # 计算 MBTI 类型
    mbti_result = calculate_mbti(results)

    # 显示测试结果解释
    print("\n您的 MBTI 测试结果：", mbti_result)
    explanation = get_mbti_explanation(mbti_result)
    print("\nMBTI 说明：\n", explanation)

    # 获取邮箱
    email = ask_email()

    if email:
        # 邮件内容包括 MBTI 测试结果及解释
        email_body = f"您好，您的 MBTI 测试结果为：{mbti_result}。\n\nMBTI 类型说明：\n{explanation}\n\n测试结果仅供参考！！！   有任何问题可邮箱与我联系！！！"
        send_email(email, email_body, email)
    else:
        print("\n跳过邮箱接收，感谢您的测试！")

    # 按任意键退出程序
    print("\n按任意键退出程序...")
    os.system("pause")  # Windows 用户
    # 对于 macOS 或 Linux 用户，可以用下面一行代替 os.system("pause")
    # input()


if __name__ == "__main__":
    main()
