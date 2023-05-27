import numpy as np
import tensorflow as tf

NUM_MFCCS = 13
MAX_LEN = 192
SAMPLE_RATE = 16000
DURATION = 1
HOP_LENGTH = 512
words = ['langit', 'butong', 'ibabaw', 'makapalit', 'lima', 'duha', 'wala', 'sukad', 'asa', 'humok', 'miingon', 'inahan', 'raman', 'dugo', 'ko', 'usba', 'hinungdan', 'busog', 'kasuko', 'giingon', 'saging', 'ulo', 'kaniya', 'tara', 'man', 'pagsulti', 'bati', 'ta', 'kamot', 'uo', 'buntag', 'lugar', 'tiya', 'laay', 'natulog', 'ilaha', 'usab', 'tatay', 'ingato', 'diin', 'basta', 'dugang', 'namo', 'unsa', 'hagad', 'bago', 'tiil', 'unta', 'ate', 'hapon', 'gahapon', 'kasabot', 'dapit', 'kinsa', 'pirmi', 'pito', 'kato', 'asawa', 'tubig', 'nanay', 'iyaha', 'dili', 'hubog', 'kana', 'maulaw', 'mao', 'dako', 'tawo', 'gutom', 'pay', 'hinuon', 'nasod', 'hilantan', 'kani', 'kuya', 'puyo', 'sakyan', 'yuta', 'mangga', 'gwapo', 'aron', 'pila', 'gawas', 'gibuhat', 'buhi', 'pakwan', 'babaye', 'sala', 'kanang', 'siya', 'amahan', 'kwarta', 'amoa', 'nabuang', 'tuo', 'sama', 'kinahanglan', 'sambag', 'kini', 'maayong', 'gani', 'salamat', 'ikaw', 'tiyo', 'gabii', 'bana', 'human', 'gamay', 'ugma', 'gwapa', 'dugay', 'pangutana', 'bukid', 'na', 'mansanas', 'kapayas', 'agi', 'bitaw', 'palihug', 'ako', 'tuig', 'tiguwang', 'buot', 'gahi', 'apan', 'bata', 'ngadto', 'oi', 'pasayloa', 'kita', 'nila', 'ah', 'lalaki', 'libo', 'didto', 'dalan', 'nahurot', 'pero', 'natagak', 'pwede', 'buwan', 'ligo', 'trabaho', 'tambis', 'upat', 'usa', 'maoy', 'ngalan', 'unom', 'balay', 'patay', 'niini', 'among', 'napu', 'amping', 'tungod', 'pinoy', 'ninyo', 'gyod', 'atis', 'unsaon', 'basin', 'kanusa', 'dungan', 'ana', 'abokado', 'atubangan', 'walo', 'may', 'tag', 'tibuok', 'siyam', 'naa', 'istorya', 'nawung', 'balita', 'lingaw', 'naman', 'bantayan', 'naligo', 'bayabas', 'buungon', 'manghuwam', 'luyo', 'unya', 'lang', 'ubos', 'sobra', 'pinaagi', 'tulo', 'kanato', 'nawong', 'hasta', 'lugara', 'buang', 'ang', 'sulod', 'edad', 'balaod', 'iya']
NUM_CLASSES = len(words)

model = tf.keras.models.load_model('weights.h5')

model.summary()
model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])