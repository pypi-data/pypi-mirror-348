from transformers import AutoConfig, AutoModel, AutoModelForMaskedLM, AutoModelForSequenceClassification, AutoModelForCausalLM, AutoModelForTokenClassification, AutoModelForQuestionAnswering, AutoModelForMultipleChoice
from .bert.modeling_bert import BertModel, BertForMaskedLM, BertForSequenceClassification, BertForQuestionAnswering, BertForMultipleChoice
from .bert.configuration_bert import BertConfig
from .gpt2.configuration_gpt2 import GPT2Config
from .gpt2.modeling_gpt2 import (
    GPT2Model,
    GPT2LMHeadModel,
    GPT2ForSequenceClassification,
    GPT2ForTokenClassification,
    GPT2ForQuestionAnswering,
    GPT2DoubleHeadsModel,
)
# uniqk bert
AutoConfig.register('uniqk/bert', BertConfig)
AutoModel.register(BertConfig, BertModel, exist_ok=True)
AutoModelForMaskedLM.register(BertConfig, BertForMaskedLM, exist_ok=True)
AutoModelForSequenceClassification.register(BertConfig, BertForSequenceClassification, exist_ok=True)
AutoModelForQuestionAnswering.register(BertConfig, BertForQuestionAnswering, exist_ok=True)
AutoModelForMultipleChoice.register(BertConfig, BertForMultipleChoice, exist_ok=True)
# uniqk gpt2
AutoConfig.register("uniqk/gpt2", GPT2Config)
AutoModel.register(GPT2Config, GPT2Model, exist_ok=True)
AutoModelForCausalLM.register(GPT2Config, GPT2LMHeadModel, exist_ok=True)
AutoModelForSequenceClassification.register(GPT2Config, GPT2ForSequenceClassification, exist_ok=True)
AutoModelForTokenClassification.register(GPT2Config, GPT2ForTokenClassification, exist_ok=True)
AutoModelForQuestionAnswering.register(GPT2Config, GPT2ForQuestionAnswering, exist_ok=True)
AutoModelForMultipleChoice.register(GPT2Config, GPT2DoubleHeadsModel, exist_ok=True)