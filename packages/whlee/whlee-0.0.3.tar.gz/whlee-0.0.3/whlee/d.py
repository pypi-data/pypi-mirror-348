import numpy as np, pandas as pd
import copy, functools, addict


from .t import timee

class dictee(dict):
    """
    反转时行为
    ----------
    要求 value 可 hash。否则请用 invert_unhashable。
    value 重复时合并，取最后出现的 key。np.nan 重复也会合并。
    输出类型仍是 idict。

    固化顺序
    --------
    输出为嵌套元组

    example
    -------
    vd = idict(name='Allen', age=np.nan, gender='male', gende=np.nan) 
    vd.invert
    vd.invert_unhashable
    vd.preserve
    vd.invert.preserve
    vd.invert_unhashable.preserve
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    @property
    def invert(self):
        return self.__class__({v: k for k, v in self.items()})
    @property
    def invert_unhashable(self):
        return self.__class__({str(v): k for k, v in self.items()})
    @property
    def preserve(self):
        return tuple(self.items())

        
# ________________________________________________________________________


class Datazz:
    def __init__(self, raw_data, target_name='y', tasktype='classification', frac='523', retaincut=False, noshuffle=False, seed=123):
        self.seed = seed
        self.raw_data = copy.deepcopy(raw_data)
        if isinstance(self.raw_data, list):  # 如果是多段数据则纵向合并。
            self.concat_data = pd.concat(self.raw_data, axis=0)
        else:
            self.concat_data = self.raw_data

        self.target_name = target_name

        if not self.concat_data.index.is_unique and not retaincut:  # 判断index是否重复
            raise ValueError('index not unique.')

        if self.concat_data[self.target_name].isna().sum() > 0:  # target中不能有np.nan或None
            raise ValueError('label contains nan value.')
        self.tasktype = tasktype
        self.frac = frac
        self.retaincut = retaincut
        self.noshuffle = noshuffle

        self.run()
        self.update_state()

    def update_state(self, ):
        self.state = addict.Dict()
        self.state.retaincut = self.retaincut
        self.state.tasktype = self.tasktype
        self.state.columns = self.concat_data.columns
        self.state.target_name = self.target_name
        self.state.frac = self.frac
        self.state.shape.concat_data = self.concat_data.shape
        self.state.shape.xy = self.xy.shape
        self.state.shape.tr = self.tr.shape
        self.state.shape.trtr = None if self.__dict__.get('trtr') is None else self.trtr.shape
        self.state.shape.val = None if not hasattr(self, 'val') else self.val.shape
        self.state.shape.te = self.te.shape

    def run(self, ):
        if self.retaincut:
            if len(self.raw_data) == 2:  # 注意这里划分验证集会受到重复index的影响，需谨慎。
                self.tr = self.raw_data[0]
                self.trtr = self.raw_data[0].sample(frac=0.8, random_state=self.seed)  # 直接写死二八划分
                self.val = self.raw_data[0].loc[self.tr.index.difference(self.trtr.index)]
                self.te = self.raw_data[1]
            elif len(self.raw_data) == 3:
                self.tr = pd.concat(self.raw_data[:2], axis=0)
                self.trtr = self.raw_data[0]
                self.val = self.raw_data[1]
                self.te = self.raw_data[2]
            self.xtr, self.ytr = self.tr.drop(columns=self.target_name), self.tr[self.target_name]
            self.xtrtr, self.ytrtr = self.trtr.drop(columns=self.target_name), self.trtr[self.target_name]
            self.xval, self.yval = self.val.drop(columns=self.target_name), self.val[self.target_name]
            self.xte, self.yte = self.te.drop(columns=self.target_name), self.te[self.target_name]
            self.x = pd.concat([self.xtr, self.xte], axis=0)
            self.y = pd.concat([self.ytr, self.yte], axis=0)
            self.xy = pd.concat([self.x, self.y], axis=1)

        elif self.noshuffle:
            if len(self.frac) == 3:  # 支持格式'523'
                fraction_train = int(self.frac[0]) / 10
                fraction_valid = int(self.frac[1]) / 10
                fraction_test = int(self.frac[2]) / 10
            elif len(self.frac) == 6:  # 支持格式'502030'
                fraction_train = int(self.frac[0:2]) / 100
                fraction_valid = int(self.frac[2:4]) / 100
                fraction_test = int(self.frac[4:6]) / 100

            if isinstance(self.noshuffle, str):
                self.concat_data = self.concat_data.sort_values(by=self.noshuffle)

            num_all = self.concat_data.shape[0]
            num_trtr = round(num_all * fraction_train)
            num_val = round(num_all * fraction_valid)
            num_te = round(num_all * fraction_test)
            if num_te > (num_all - num_trtr - num_val):
                num_te = (num_all - num_trtr - num_val)

            self.tr = self.concat_data.iloc[: num_trtr + num_val]
            self.trtr = self.concat_data.iloc[: num_trtr]
            self.val = self.concat_data.iloc[num_trtr: num_trtr + num_val]
            self.te = self.concat_data.iloc[num_trtr + num_val: num_trtr + num_val + num_te]
            self.xtr, self.ytr = self.tr.drop(columns=self.target_name), self.tr[self.target_name]
            self.xtrtr, self.ytrtr = self.trtr.drop(columns=self.target_name), self.trtr[self.target_name]
            self.xval, self.yval = self.val.drop(columns=self.target_name), self.val[self.target_name]
            self.xte, self.yte = self.te.drop(columns=self.target_name), self.te[self.target_name]
            self.x = pd.concat([self.xtr, self.xte], axis=0)
            self.y = pd.concat([self.ytr, self.yte], axis=0)
            self.xy = pd.concat([self.x, self.y], axis=1)

        else:
            if self.tasktype == 'regression':  # 分类与回归的本质就是一个分层抽样一个不分层抽样。
                self.index_trtr, self.index_val, self.index_te = self.split3(self.concat_data, frac=self.frac, seed=self.seed)
            elif self.tasktype == 'classification':
                dflist = [grp[1] for grp in self.concat_data.groupby(self.target_name)]
                tmp = [self.split3(df, frac=self.frac, seed=self.seed) for df in dflist]  # 对每个df分别split
                self.index_trtr, self.index_val, self.index_te = [functools.reduce(lambda x, y: x.append(y), index_list)
                                                                  for index_list in zip(*tmp)]  # 行列转换
            self.tr = self.concat_data.loc[self.index_trtr.append(self.index_val)]
            self.trtr = self.concat_data.loc[self.index_trtr]
            self.val = self.concat_data.loc[self.index_val]
            self.te = self.concat_data.loc[self.index_te]
            self.xtr, self.ytr = self.tr.drop(columns=self.target_name), self.tr[self.target_name]
            self.xtrtr, self.ytrtr = self.trtr.drop(columns=self.target_name), self.trtr[self.target_name]
            self.xval, self.yval = self.val.drop(columns=self.target_name), self.val[self.target_name]
            self.xte, self.yte = self.te.drop(columns=self.target_name), self.te[self.target_name]
            self.x = pd.concat([self.xtr, self.xte], axis=0)
            self.y = pd.concat([self.ytr, self.yte], axis=0)
            self.xy = pd.concat([self.x, self.y], axis=1)

        self.index_xy = self.xy.index
        self.index_tr = self.tr.index
        self.index_trtr = self.trtr.index
        self.index_val = self.val.index
        self.index_te = self.te.index

    @staticmethod
    def split3(df, frac, seed):  # 给出的比例总合不能大于1
        if len(frac) == 3:  # 支持格式'523'
            fraction_train = int(frac[0]) / 10
            fraction_valid = int(frac[1]) / 10
            fraction_test = int(frac[2]) / 10
        elif len(frac) == 6:  # 支持格式'502030'
            fraction_train = int(frac[0:2]) / 100
            fraction_valid = int(frac[2:4]) / 100
            fraction_test = int(frac[4:6]) / 100
        index_all = df.index
        index_train = df.sample(frac=fraction_train, random_state=seed).index
        index_train_inverse = index_all.difference(index_train)
        index_valid = df.loc[index_train_inverse].sample(frac=fraction_valid / (1 - fraction_train), random_state=seed).index
        index_train_valid = pd.Index.append(index_train, index_valid)
        index_train_valid_inverse = index_all.difference(index_train_valid)
        tmp_frac = round(fraction_test / (1 - fraction_train - fraction_valid), 10)  # 因精度问题，需要抹平10个零后的小数点，否则会超过1。
        index_test = df.loc[index_train_valid_inverse].sample(frac=tmp_frac, random_state=seed).index
        return index_train, index_valid, index_test

    def transfer_colnames(self, new_cols=None, target_name=None):
        def rename(df, new):
            if isinstance(new, list):
                df.columns = new
            elif isinstance(new, dict):
                df.rename(columns=new, inplace=True)
            return df

        if new_cols:
            if isinstance(self.raw_data, pd.core.frame.DataFrame):
                self.raw_data = rename(self.raw_data, new_cols)
            elif isinstance(self.raw_data, list):
                self.raw_data = [rename(df, new_cols) for df in self.raw_data]
            self.concat_data = rename(self.concat_data, new_cols)
        if target_name:
            self.target_name = target_name
        print(list(self.concat_data))
        self.run()
        self.update_state()

    def balance_blend(self, set_name='tr'):  # 可用于2分类和多分类的均衡，按照倒数第2多类别与倒数第1多类别的地板比例决定训练集个数。
        if not self.tasktype == 'classification':
            raise TypeError('tasktype must be cls.')
        data = eval('self.' + set_name)
        target_name = self.target_name
        ct_sorted = sorted(collections.Counter(data[target_name]).items(), key=lambda x: x[1])
        ultimate = ct_sorted[0][1]
        penultimate = ct_sorted[1][1]
        n = int(np.floor(penultimate / ultimate))
        train_detach = [data[data[target_name] == i[0]] for i in ct_sorted]
        train_datasets = []
        for i in range(n):
            dt = [detach[ultimate * i: ultimate * (i + 1)] for detach in train_detach[1:]] + [train_detach[0]]
            dataset = pd.concat(dt, axis=0)
            train_datasets.append(dataset)
        self.train_datasets = train_datasets
        self.state.balance = ('balance_blend', len(self.train_datasets), self.train_datasets[0].shape)


# ________________________________________________________________________


assistant = """You are a helpful assistant."""
news2json = """用户将提供给你一段新闻内容，请你分析新闻内容，并提取其中的关键信息，以 JSON 的形式输出，输出的 JSON 需遵守以下的格式：
{
  "entity": <新闻实体>,
  "time": <新闻时间，格式为 YYYY-mm-dd HH:MM:SS，没有请填 null>,
  "summary": <新闻内容总结>
}"""
cosplay = """请你扮演一个刚从美国留学回国的人，说话时候会故意中文夹杂部分英文单词，显得非常fancy，对话中总是带有很强的优越感。"""
outline = """你是一位文本大纲生成专家，擅长根据用户的需求创建一个有条理且易于扩展成完整文章的大纲，你拥有强大的主题分析能力，能准确提取关键信息和核心要点。具备丰富的文案写作知识储备，熟悉各种文体和题材的文案大纲构建方法。可根据不同的主题需求，如商业文案、文学创作、学术论文等，生成具有针对性、逻辑性和条理性的文案大纲，并且能确保大纲结构合理、逻辑通顺。该大纲应该包含以下部分：
            引言：介绍主题背景，阐述撰写目的，并吸引读者兴趣。
            主体部分：第一段落：详细说明第一个关键点或论据，支持观点并引用相关数据或案例。
            第二段落：深入探讨第二个重点，继续论证或展开叙述，保持内容的连贯性和深度。
            第三段落：如果有必要，进一步讨论其他重要方面，或者提供不同的视角和证据。
            结论：总结所有要点，重申主要观点，并给出有力的结尾陈述，可以是呼吁行动、提出展望或其他形式的收尾。
            创意性标题：为文章构思一个引人注目的标题，确保它既反映了文章的核心内容又能激发读者的好奇心。"""
slogan = """你是一个宣传标语专家，请根据用户需求设计一个独具创意且引人注目的宣传标语，需结合该产品/活动的核心价值和特点，同时融入新颖的表达方式或视角。请确保标语能够激发潜在客户的兴趣，并能留下深刻印象，可以考虑采用比喻、双关或其他修辞手法来增强语言的表现力。标语应简洁明了，需要朗朗上口，易于理解和记忆，一定要押韵，不要太过书面化。只输出宣传标语，不用解释。"""
translator = """你是一个中英文翻译专家，将用户输入的中文翻译成英文，或将用户输入的英文翻译成中文。对于非中文内容，它将提供中文翻译结果。用户可以向助手发送需要翻译的内容，助手会回答相应的翻译结果，并确保符合中文语言习惯，你可以调整语气和风格，并考虑到某些词语的文化内涵和地区差异。同时作为翻译家，需将原文翻译成具有信达雅标准的译文。"信" 即忠实于原文的内容与意图；"达" 意味着译文应通顺易懂，表达清晰；"雅" 则追求译文的文化审美和语言的优美。目标是创作出既忠于原作精神，又符合目标语言文化和读者审美的翻译。"""
english_teacher = """请你扮演一个英文老师，使用英语和学生进行对话练习。具体要求如下：
（1）只使用英语进行交流。
（2）词汇量控制在最常用的 500 个以内，要足够简单到幼儿园小朋友可以理解。
（3）如果对方在交流中出现英文使用错语，要马上提示对方错误点，并告诉对方如何改正。然后再回到之前的英文交流主题。
（4）提示的错语包括拼写错误、时态错误、句子语法不精确、词义不准确等，但是不包括首字母大小写。
（5）英文交流主题限制在体育运动方面，可以是各种运动。如果对方跑题要想办法把话题拉回来。
（6）如果对方使用中文表达，请帮助学生将中文转换成英文，并提醒对方继续使用英文表达。"""
system_roles = {'assistant': assistant, 'news2json': news2json, 'cosplay': cosplay, 'outline': outline, 'slogan': slogan, 'translator': translator, 'english_teacher': english_teacher, '': None, }


念奴娇 = """以苏轼的口吻，给千年后自己的研究者写一首词，用“念奴娇”词牌。"""
情景续写 = """假设诸葛亮死后在地府遇到了刘备，请模拟两个人展开一段对话。"""
散文写作 = """以孤独的夜行者为题写一篇750字的散文，描绘一个人在城市中夜晚漫无目的行走的心情与所见所感，以及夜的寂静给予的独特感悟。"""
诗歌创作 = """模仿李白的风格写一首七律.飞机"""
prompts = {'念奴娇': 念奴娇, '情景续写': 情景续写, '散文写作': 散文写作, '诗歌创作': 诗歌创作, '': None, }

class DS:
    """
    ds = DS(system_roles=system_roles, prompts=prompts)
    ds.restart()  # 重启对话
    
    # 例用默认的 system role。将添加 {'role': 'system', 'content': "You are a helpful assistant."}
    rst = ds.chat('2的平方是？')
    
    # 不使用 system role，令 role=None 不加系统角色。
    rst = ds.chat('2的平方是？', role=None)
    
    # 例用深度思考
    rst = ds.chat('2的平方是？', r1=True)
    
    # 追问（不再设置 system role）
    rst = ds.inquire('3呢')

    # 中英翻译专家（自动识别中英文）
    rst = ds.chat('你好吗？', role='translator')

    # 英文老师
    ds = DS(system_roles=system_roles, prompts=prompts)
    rst = ds.chat('你好吗？', role='english_teacher')
    rst = ds.inquire('我想想')

    # 宣传标语生成
    rst = ds.chat('请生成“希腊酸奶”的宣传标语', role='slogan')
    
    # 角色扮演之自定义人设美国留学生
    rst = ds.chat('美国的饮食还习惯么。', role='cosplay')

    # 结构化输出 json
    content = "8月31日，一枚猎鹰9号运载火箭于美国东部时间凌晨3时43分从美国佛罗里达州卡纳维拉尔角发射升空，将21颗星链卫星（Starlink）送入轨道。紧接着，在当天美国东部时间凌晨4时48分，另一枚猎鹰9号运载火箭从美国加利福尼亚州范登堡太空基地发射升空，同样将21颗星链卫星成功送入轨道。两次发射间隔65分钟创猎鹰9号运载火箭最短发射间隔纪录。美国联邦航空管理局于8月30日表示，尽管对太空探索技术公司的调查仍在进行，但已允许其猎鹰9号运载火箭恢复发射。目前，双方并未透露8月28日助推器着陆失败事故的详细信息。尽管发射已恢复，但原计划进行五天太空活动的“北极星黎明”（Polaris Dawn）任务却被推迟。美国太空探索技术公司为该任务正在积极筹备，等待美国联邦航空管理局的最终批准后尽快进行发射。"
    rst = ds.chat(content, role='news2json')

    # 文案大纲生成
    rst = ds.chat('请帮我生成“中国农业情况”这篇文章的大纲', role='outline')
    
    # 属性
    ds.messages
    ds.response.choices[0].message.content
    ds.response.choices[0].message.reasoning_content  # 深度思考

    """
    def __init__(self, api_key, base_url, system_roles=system_roles, prompts=prompts, time_print=False):
        from openai import OpenAI
        # 固定属性
        self.client = OpenAI(api_key=api_key, base_url=base_url)
        self.system_roles = system_roles  # 加截角色配置
        self.prompts = prompts  # 加截经典提示词
        self.r1 = False  # 是否使用 R1 深度思考。每次使用后，都会自动重置为 False。
        # 变化属性
        self.messages = []  # input tokens
        self.response = None  # output tokens

        if time_print:  # 是否打印执行时间，timee是个装饰器。
            self.chat = timee(self.chat)
            self.inquire = timee(self.inquire)
        
    def template(self, prompt, kind='role_user', r1=False):  # 上层封装模板 template
        """
        # 上层模板应用
        ds = DS(system_roles=system_roles, prompts=prompts)
        rst = ds.template(prompt='念奴娇', kind='role_user')  # role_user直接问的模板
        rst = ds.template(prompt='common, normal, ', kind='compare')
        """
        self.r1 = True if r1 else False  # 深度思考开关，每次执行使用默认值，都会关闭 R1
        if kind=='role_user':  # 直接问，不用 system role
            return self.chat(content=self.prompts[prompt], role=None)
        elif kind=='compare':  # 对比几个单词用法上的差异
            prompt = f"{prompt}，请分析一下这几个相近单词在意思上的区别，并分别提供一个便于理解的例子。"
            return self.chat(content=prompt, role=None)
        else:
            pass
            
    def chat(self, content, role='assistant', r1=False):  # 默认使用 role='assistant'。如果不想使用 system_role，则令 role=None
        self.r1 = True if r1 else False  # 深度思考开关
        if role:  # 使用 system_role
            role_content = self.system_roles[role]
            system_role = {'role': 'system', 'content': role_content}
            self.messages.append(system_role)
        else:  # 不使用 system_role
            pass
        user_content = {'role': 'user', 'content': content}
        self.messages.append(user_content)
        self.send()
        return self.response.choices[0].message.content
        
    def inquire(self, content, r1=False):  # 多轮对话，不需要再设置
        self.r1 = True if r1 else False  # 深度思考开关
        self.messages.append(self.response.choices[0].message)
        user_content = {'role': 'user', 'content': content}
        self.messages.append(user_content)
        self.send()
        return self.response.choices[0].message.content
        
    def send(self):
        if self.r1 == False:  # 不使用深度思考
            model='deepseek-chat'
        elif self.r1 == True:  # 使用深度思考
            model='deepseek-reasoner'
            self.r1 = False
        self.response = self.client.chat.completions.create(model=model, messages=self.messages, stream=False)

    def restart(self):  # 重置对话
        self.messages = []
        self.response = None



