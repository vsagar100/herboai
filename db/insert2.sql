INSERT INTO plant_synonyms (plant_id, synonym, language, kind)
SELECT p.id, s.synonym, s.language, s.kind
FROM plants p
JOIN (
    --------------------------------------------------------------------
    -- 31. Zingiber officinale – Dry Ginger / Shunthi
    --------------------------------------------------------------------
    SELECT 'Zingiber officinale' AS botanical_name, 'Dry Ginger' AS synonym, 'en' AS language, 'common_name' AS kind
    UNION ALL SELECT 'Zingiber officinale','Shunthi','en','classical_name'
    UNION ALL SELECT 'Zingiber officinale','सूखी अदरक','hi','common_name'
    UNION ALL SELECT 'Zingiber officinale','सुंठ','mr','common_name'

    --------------------------------------------------------------------
    -- 32. Curcuma zedoaria – Kachur / White Turmeric
    --------------------------------------------------------------------
    UNION ALL SELECT 'Curcuma zedoaria','Kachur','en','common_name'
    UNION ALL SELECT 'Curcuma zedoaria','White Turmeric','en','common_name'
    UNION ALL SELECT 'Curcuma zedoaria','कचूर','hi','common_name'
    UNION ALL SELECT 'Curcuma zedoaria','कचूर','mr','common_name'

    --------------------------------------------------------------------
    -- 33. Cinnamomum verum – Cinnamon
    --------------------------------------------------------------------
    UNION ALL SELECT 'Cinnamomum verum','Cinnamon','en','common_name'
    UNION ALL SELECT 'Cinnamomum verum','True Cinnamon','en','common_name'
    UNION ALL SELECT 'Cinnamomum verum','दालचीनी','hi','common_name'
    UNION ALL SELECT 'Cinnamomum verum','दालचिनी','mr','common_name'

    --------------------------------------------------------------------
    -- 34. Syzygium aromaticum – Clove
    --------------------------------------------------------------------
    UNION ALL SELECT 'Syzygium aromaticum','Clove','en','common_name'
    UNION ALL SELECT 'Syzygium aromaticum','Lavang','en','common_name'
    UNION ALL SELECT 'Syzygium aromaticum','लौंग','hi','common_name'
    UNION ALL SELECT 'Syzygium aromaticum','लवंग','mr','common_name'

    --------------------------------------------------------------------
    -- 35. Elettaria cardamomum – Green Cardamom
    --------------------------------------------------------------------
    UNION ALL SELECT 'Elettaria cardamomum','Green Cardamom','en','common_name'
    UNION ALL SELECT 'Elettaria cardamomum','Elaichi','en','common_name'
    UNION ALL SELECT 'Elettaria cardamomum','छोटी इलायची','hi','common_name'
    UNION ALL SELECT 'Elettaria cardamomum','वेलची','mr','common_name'

    --------------------------------------------------------------------
    -- 36. Foeniculum vulgare – Fennel
    --------------------------------------------------------------------
    UNION ALL SELECT 'Foeniculum vulgare','Fennel','en','common_name'
    UNION ALL SELECT 'Foeniculum vulgare','Saunf','en','common_name'
    UNION ALL SELECT 'Foeniculum vulgare','सौंफ','hi','common_name'
    UNION ALL SELECT 'Foeniculum vulgare','बडीशेप','mr','common_name'

    --------------------------------------------------------------------
    -- 37. Cuminum cyminum – Cumin
    --------------------------------------------------------------------
    UNION ALL SELECT 'Cuminum cyminum','Cumin','en','common_name'
    UNION ALL SELECT 'Cuminum cyminum','Jeera','en','common_name'
    UNION ALL SELECT 'Cuminum cyminum','जीरा','hi','common_name'
    UNION ALL SELECT 'Cuminum cyminum','जिरे','mr','common_name'

    --------------------------------------------------------------------
    -- 38. Coriandrum sativum – Coriander
    --------------------------------------------------------------------
    UNION ALL SELECT 'Coriandrum sativum','Coriander','en','common_name'
    UNION ALL SELECT 'Coriandrum sativum','Cilantro','en','common_name'
    UNION ALL SELECT 'Coriandrum sativum','धनिया','hi','common_name'
    UNION ALL SELECT 'Coriandrum sativum','कोथिंबीर','mr','common_name'

    --------------------------------------------------------------------
    -- 39. Trachyspermum ammi – Ajwain
    --------------------------------------------------------------------
    UNION ALL SELECT 'Trachyspermum ammi','Ajwain','en','common_name'
    UNION ALL SELECT 'Trachyspermum ammi','Carom Seed','en','common_name'
    UNION ALL SELECT 'Trachyspermum ammi','अजवाइन','hi','common_name'
    UNION ALL SELECT 'Trachyspermum ammi','ओवा','mr','common_name'

    --------------------------------------------------------------------
    -- 40. Trigonella foenum-graecum – Fenugreek
    --------------------------------------------------------------------
    UNION ALL SELECT 'Trigonella foenum-graecum','Fenugreek','en','common_name'
    UNION ALL SELECT 'Trigonella foenum-graecum','Methi','en','common_name'
    UNION ALL SELECT 'Trigonella foenum-graecum','मेथी','hi','common_name'
    UNION ALL SELECT 'Trigonella foenum-graecum','मेथी','mr','common_name'

    --------------------------------------------------------------------
    -- 41. Nigella sativa – Black Seed
    --------------------------------------------------------------------
    UNION ALL SELECT 'Nigella sativa','Black Seed','en','common_name'
    UNION ALL SELECT 'Nigella sativa','Kalonji','en','common_name'
    UNION ALL SELECT 'Nigella sativa','कलौंजी','hi','common_name'
    UNION ALL SELECT 'Nigella sativa','कलौंजी','mr','common_name'

    --------------------------------------------------------------------
    -- 42. Pimpinella anisum – Anise
    --------------------------------------------------------------------
    UNION ALL SELECT 'Pimpinella anisum','Anise','en','common_name'
    UNION ALL SELECT 'Pimpinella anisum','Aniseed','en','common_name'
    UNION ALL SELECT 'Pimpinella anisum','अनीस','hi','common_name'
    UNION ALL SELECT 'Pimpinella anisum','अनिस','mr','common_name'

    --------------------------------------------------------------------
    -- 43. Carum carvi – Caraway
    --------------------------------------------------------------------
    UNION ALL SELECT 'Carum carvi','Caraway','en','common_name'
    UNION ALL SELECT 'Carum carvi','Shah Jeera','en','common_name'
    UNION ALL SELECT 'Carum carvi','काला जीरा','hi','common_name'
    UNION ALL SELECT 'Carum carvi','शाहजिरे','mr','common_name'

    --------------------------------------------------------------------
    -- 44. Chrysopogon zizanioides – Vetiver
    --------------------------------------------------------------------
    UNION ALL SELECT 'Chrysopogon zizanioides','Vetiver','en','common_name'
    UNION ALL SELECT 'Chrysopogon zizanioides','Khus Root','en','common_name'
    UNION ALL SELECT 'Chrysopogon zizanioides','खस','hi','common_name'
    UNION ALL SELECT 'Chrysopogon zizanioides','उशीर','mr','common_name'

    --------------------------------------------------------------------
    -- 45. Santalum album – Sandalwood
    --------------------------------------------------------------------
    UNION ALL SELECT 'Santalum album','Sandalwood','en','common_name'
    UNION ALL SELECT 'Santalum album','White Sandalwood','en','common_name'
    UNION ALL SELECT 'Santalum album','चंदन','hi','common_name'
    UNION ALL SELECT 'Santalum album','चंदन','mr','common_name'

    --------------------------------------------------------------------
    -- 46. Nelumbo nucifera – Lotus
    --------------------------------------------------------------------
    UNION ALL SELECT 'Nelumbo nucifera','Lotus','en','common_name'
    UNION ALL SELECT 'Nelumbo nucifera','Sacred Lotus','en','common_name'
    UNION ALL SELECT 'Nelumbo nucifera','कमल','hi','common_name'
    UNION ALL SELECT 'Nelumbo nucifera','कमळ','mr','common_name'

    --------------------------------------------------------------------
    -- 47. Nymphaea stellata – Blue Water Lily
    --------------------------------------------------------------------
    UNION ALL SELECT 'Nymphaea stellata','Blue Water Lily','en','common_name'
    UNION ALL SELECT 'Nymphaea stellata','Nilkamal','en','common_name'
    UNION ALL SELECT 'Nymphaea stellata','नील कमल','hi','common_name'
    UNION ALL SELECT 'Nymphaea stellata','नील कमळ','mr','common_name'

    --------------------------------------------------------------------
    -- 48. Ficus religiosa – Peepal
    --------------------------------------------------------------------
    UNION ALL SELECT 'Ficus religiosa','Peepal','en','common_name'
    UNION ALL SELECT 'Ficus religiosa','Sacred Fig','en','common_name'
    UNION ALL SELECT 'Ficus religiosa','पीपल','hi','common_name'
    UNION ALL SELECT 'Ficus religiosa','पिंपळ','mr','common_name'

    --------------------------------------------------------------------
    -- 49. Ficus benghalensis – Banyan
    --------------------------------------------------------------------
    UNION ALL SELECT 'Ficus benghalensis','Banyan','en','common_name'
    UNION ALL SELECT 'Ficus benghalensis','Indian Banyan','en','common_name'
    UNION ALL SELECT 'Ficus benghalensis','बरगद','hi','common_name'
    UNION ALL SELECT 'Ficus benghalensis','वड','mr','common_name'

    --------------------------------------------------------------------
    -- 50. Ficus racemosa – Cluster Fig
    --------------------------------------------------------------------
    UNION ALL SELECT 'Ficus racemosa','Cluster Fig','en','common_name'
    UNION ALL SELECT 'Ficus racemosa','Gular','en','common_name'
    UNION ALL SELECT 'Ficus racemosa','गूलर','hi','common_name'
    UNION ALL SELECT 'Ficus racemosa','उंबर','mr','common_name'

    --------------------------------------------------------------------
    -- 51. Musa paradisiaca – Plantain
    --------------------------------------------------------------------
    UNION ALL SELECT 'Musa paradisiaca','Plantain','en','common_name'
    UNION ALL SELECT 'Musa paradisiaca','Raw Banana','en','common_name'
    UNION ALL SELECT 'Musa paradisiaca','कच्चा केला','hi','common_name'
    UNION ALL SELECT 'Musa paradisiaca','रावळे केळी','mr','common_name'

    --------------------------------------------------------------------
    -- 52. Punica granatum – Pomegranate
    --------------------------------------------------------------------
    UNION ALL SELECT 'Punica granatum','Pomegranate','en','common_name'
    UNION ALL SELECT 'Punica granatum','Anar','en','common_name'
    UNION ALL SELECT 'Punica granatum','अनार','hi','common_name'
    UNION ALL SELECT 'Punica granatum','डाळिंब','mr','common_name'

    --------------------------------------------------------------------
    -- 53. Cocos nucifera – Coconut
    --------------------------------------------------------------------
    UNION ALL SELECT 'Cocos nucifera','Coconut','en','common_name'
    UNION ALL SELECT 'Cocos nucifera','Nariyal','en','common_name'
    UNION ALL SELECT 'Cocos nucifera','नारियल','hi','common_name'
    UNION ALL SELECT 'Cocos nucifera','नारळ','mr','common_name'

    --------------------------------------------------------------------
    -- 54. Sesamum indicum – Sesame
    --------------------------------------------------------------------
    UNION ALL SELECT 'Sesamum indicum','Sesame','en','common_name'
    UNION ALL SELECT 'Sesamum indicum','Til','en','common_name'
    UNION ALL SELECT 'Sesamum indicum','तिल','hi','common_name'
    UNION ALL SELECT 'Sesamum indicum','तिळ','mr','common_name'

    --------------------------------------------------------------------
    -- 55. Linum usitatissimum – Flax
    --------------------------------------------------------------------
    UNION ALL SELECT 'Linum usitatissimum','Flax','en','common_name'
    UNION ALL SELECT 'Linum usitatissimum','Alsi','en','common_name'
    UNION ALL SELECT 'Linum usitatissimum','अलसी','hi','common_name'
    UNION ALL SELECT 'Linum usitatissimum','जवस','mr','common_name'

    --------------------------------------------------------------------
    -- 56. Ricinus communis – Castor
    --------------------------------------------------------------------
    UNION ALL SELECT 'Ricinus communis','Castor','en','common_name'
    UNION ALL SELECT 'Ricinus communis','Castor Oil Plant','en','common_name'
    UNION ALL SELECT 'Ricinus communis','अरंडी','hi','common_name'
    UNION ALL SELECT 'Ricinus communis','एरंड','mr','common_name'

    --------------------------------------------------------------------
    -- 57. Pongamia pinnata – Karanja
    --------------------------------------------------------------------
    UNION ALL SELECT 'Pongamia pinnata','Karanja','en','common_name'
    UNION ALL SELECT 'Pongamia pinnata','Indian Beech','en','common_name'
    UNION ALL SELECT 'Pongamia pinnata','करंज','hi','common_name'
    UNION ALL SELECT 'Pongamia pinnata','कऱंज','mr','common_name'

    --------------------------------------------------------------------
    -- 58. Murraya koenigii – Curry Leaf
    --------------------------------------------------------------------
    UNION ALL SELECT 'Murraya koenigii','Curry Leaf','en','common_name'
    UNION ALL SELECT 'Murraya koenigii','Kadi Patta','en','common_name'
    UNION ALL SELECT 'Murraya koenigii','कड़ी पत्ता','hi','common_name'
    UNION ALL SELECT 'Murraya koenigii','कढीपत्ता','mr','common_name'

    --------------------------------------------------------------------
    -- 59. Lawsonia inermis – Henna
    --------------------------------------------------------------------
    UNION ALL SELECT 'Lawsonia inermis','Henna','en','common_name'
    UNION ALL SELECT 'Lawsonia inermis','Mehendi','en','common_name'
    UNION ALL SELECT 'Lawsonia inermis','मेहंदी','hi','common_name'
    UNION ALL SELECT 'Lawsonia inermis','मेहेंदी','mr','common_name'

    --------------------------------------------------------------------
    -- 60. Aloe vera – Aloe
    --------------------------------------------------------------------
    UNION ALL SELECT 'Aloe vera','Aloe','en','common_name'
    UNION ALL SELECT 'Aloe vera','Aloe Vera','en','common_name'
    UNION ALL SELECT 'Aloe vera','घृतकुमारी','hi','common_name'
    UNION ALL SELECT 'Aloe vera','कोरफड','mr','common_name'

    --------------------------------------------------------------------
    -- 61. Cassia fistula – Golden Shower Tree / Amaltas
    --------------------------------------------------------------------
    UNION ALL SELECT 'Cassia fistula','Golden Shower Tree','en','common_name'
    UNION ALL SELECT 'Cassia fistula','Amaltas','en','common_name'
    UNION ALL SELECT 'Cassia fistula','अमलतास','hi','common_name'
    UNION ALL SELECT 'Cassia fistula','बहावा','mr','common_name'

    --------------------------------------------------------------------
    -- 62. Holarrhena pubescens – Kutaja
    --------------------------------------------------------------------
    UNION ALL SELECT 'Holarrhena pubescens','Kutaja','en','common_name'
    UNION ALL SELECT 'Holarrhena pubescens','Kurchi','en','common_name'
    UNION ALL SELECT 'Holarrhena pubescens','कुटज','hi','common_name'
    UNION ALL SELECT 'Holarrhena pubescens','कुटज','mr','common_name'

    --------------------------------------------------------------------
    -- 63. Hygrophila auriculata – Kokilaksha
    --------------------------------------------------------------------
    UNION ALL SELECT 'Hygrophila auriculata','Kokilaksha','en','common_name'
    UNION ALL SELECT 'Hygrophila auriculata','Talmakhana','en','common_name'
    UNION ALL SELECT 'Hygrophila auriculata','तलमखाना','hi','common_name'
    UNION ALL SELECT 'Hygrophila auriculata','तालमखाना','mr','common_name'

    --------------------------------------------------------------------
    -- 64. Morinda citrifolia – Noni
    --------------------------------------------------------------------
    UNION ALL SELECT 'Morinda citrifolia','Noni','en','common_name'
    UNION ALL SELECT 'Morinda citrifolia','Indian Noni','en','common_name'
    UNION ALL SELECT 'Morinda citrifolia','नोनी','hi','common_name'
    UNION ALL SELECT 'Morinda citrifolia','नॉनी','mr','common_name'

    --------------------------------------------------------------------
    -- 65. Achyranthes aspera – Apamarga
    --------------------------------------------------------------------
    UNION ALL SELECT 'Achyranthes aspera','Apamarga','en','common_name'
    UNION ALL SELECT 'Achyranthes aspera','Prickly Chaff Flower','en','common_name'
    UNION ALL SELECT 'Achyranthes aspera','अपामार्ग','hi','common_name'
    UNION ALL SELECT 'Achyranthes aspera','अघाडा','mr','common_name'

    --------------------------------------------------------------------
    -- 66. Pterocarpus santalinus – Red Sandalwood
    --------------------------------------------------------------------
    UNION ALL SELECT 'Pterocarpus santalinus','Red Sandalwood','en','common_name'
    UNION ALL SELECT 'Pterocarpus santalinus','Rakta Chandan','en','common_name'
    UNION ALL SELECT 'Pterocarpus santalinus','रक्तचंदन','hi','common_name'
    UNION ALL SELECT 'Pterocarpus santalinus','रक्तचंदन','mr','common_name'

    --------------------------------------------------------------------
    -- 67. Cissampelos pareira – Patha
    --------------------------------------------------------------------
    UNION ALL SELECT 'Cissampelos pareira','Patha','en','common_name'
    UNION ALL SELECT 'Cissampelos pareira','Velvetleaf Creeper','en','common_name'
    UNION ALL SELECT 'Cissampelos pareira','पाठा','hi','common_name'
    UNION ALL SELECT 'Cissampelos pareira','पाठा','mr','common_name'

    --------------------------------------------------------------------
    -- 68. Hedychium spicatum – Shati
    --------------------------------------------------------------------
    UNION ALL SELECT 'Hedychium spicatum','Shati','en','common_name'
    UNION ALL SELECT 'Hedychium spicatum','Spiked Ginger Lily','en','common_name'
    UNION ALL SELECT 'Hedychium spicatum','शाठी','hi','common_name'
    UNION ALL SELECT 'Hedychium spicatum','शाठी','mr','common_name'

    --------------------------------------------------------------------
    -- 69. Berberis aristata – Daruharidra
    --------------------------------------------------------------------
    UNION ALL SELECT 'Berberis aristata','Daruharidra','en','common_name'
    UNION ALL SELECT 'Berberis aristata','Indian Barberry','en','common_name'
    UNION ALL SELECT 'Berberis aristata','दारुहल्दी','hi','common_name'
    UNION ALL SELECT 'Berberis aristata','दारुहलद','mr','common_name'

    --------------------------------------------------------------------
    -- 70. Swertia chirayita – Chirayata
    --------------------------------------------------------------------
    UNION ALL SELECT 'Swertia chirayita','Chirayata','en','common_name'
    UNION ALL SELECT 'Swertia chirayita','Kiratatikta','en','classical_name'
    UNION ALL SELECT 'Swertia chirayita','चिरायता','hi','common_name'
    UNION ALL SELECT 'Swertia chirayita','चिरायटा','mr','common_name'

    --------------------------------------------------------------------
    -- 71. Alpinia galanga – Galangal
    --------------------------------------------------------------------
    UNION ALL SELECT 'Alpinia galanga','Galangal','en','common_name'
    UNION ALL SELECT 'Alpinia galanga','Kulanjan','en','common_name'
    UNION ALL SELECT 'Alpinia galanga','कुलंजन','hi','common_name'
    UNION ALL SELECT 'Alpinia galanga','कुळंजन','mr','common_name'

    --------------------------------------------------------------------
    -- 72. Cyperus scariosus – Nagarmotha (Scariosus)
    --------------------------------------------------------------------
    UNION ALL SELECT 'Cyperus scariosus','Nagarmotha','en','common_name'
    UNION ALL SELECT 'Cyperus scariosus','Nutgrass','en','common_name'
    UNION ALL SELECT 'Cyperus scariosus','नागरमोथा','hi','common_name'
    UNION ALL SELECT 'Cyperus scariosus','नागरमोथा','mr','common_name'

    --------------------------------------------------------------------
    -- 73. Abies webbiana – Talispatra
    --------------------------------------------------------------------
    UNION ALL SELECT 'Abies webbiana','Talispatra','en','common_name'
    UNION ALL SELECT 'Abies webbiana','Indian Silver Fir','en','common_name'
    UNION ALL SELECT 'Abies webbiana','तालीसपत्र','hi','common_name'
    UNION ALL SELECT 'Abies webbiana','तालीसपत्र','mr','common_name'

    --------------------------------------------------------------------
    -- 74. Inula racemosa – Pushkarmoola
    --------------------------------------------------------------------
    UNION ALL SELECT 'Inula racemosa','Pushkarmoola','en','common_name'
    UNION ALL SELECT 'Inula racemosa','Inula Root','en','common_name'
    UNION ALL SELECT 'Inula racemosa','पुष्करमूल','hi','common_name'
    UNION ALL SELECT 'Inula racemosa','पुष्करमुळ','mr','common_name'

    --------------------------------------------------------------------
    -- 75. Solanum nigrum – Black Nightshade
    --------------------------------------------------------------------
    UNION ALL SELECT 'Solanum nigrum','Black Nightshade','en','common_name'
    UNION ALL SELECT 'Solanum nigrum','Makoy','en','common_name'
    UNION ALL SELECT 'Solanum nigrum','मकोय','hi','common_name'
    UNION ALL SELECT 'Solanum nigrum','ढोबळी भाजी','mr','common_name'

    --------------------------------------------------------------------
    -- 76. Pueraria tuberosa – Vidarikand
    --------------------------------------------------------------------
    UNION ALL SELECT 'Pueraria tuberosa','Vidarikand','en','common_name'
    UNION ALL SELECT 'Pueraria tuberosa','Indian Kudzu','en','common_name'
    UNION ALL SELECT 'Pueraria tuberosa','विदारीकंद','hi','common_name'
    UNION ALL SELECT 'Pueraria tuberosa','विदारी','mr','common_name'

    --------------------------------------------------------------------
    -- 77. Pistacia integerrima – Karkatashringi
    --------------------------------------------------------------------
    UNION ALL SELECT 'Pistacia integerrima','Karkatashringi','en','common_name'
    UNION ALL SELECT 'Pistacia integerrima','Galls of Pistacia','en','common_name'
    UNION ALL SELECT 'Pistacia integerrima','कर्कटशृंगी','hi','common_name'
    UNION ALL SELECT 'Pistacia integerrima','कर्कटशृंगी','mr','common_name'

    --------------------------------------------------------------------
    -- 78. Centratherum anthelminticum – Kalijiri
    --------------------------------------------------------------------
    UNION ALL SELECT 'Centratherum anthelminticum','Kalijiri','en','common_name'
    UNION ALL SELECT 'Centratherum anthelminticum','Bitter Cumin','en','common_name'
    UNION ALL SELECT 'Centratherum anthelminticum','काली जीरी','hi','common_name'
    UNION ALL SELECT 'Centratherum anthelminticum','काळी जिरं','mr','common_name'

    --------------------------------------------------------------------
    -- 79. Hemidesmus indicus – Indian Sarsaparilla / Sariva
    --------------------------------------------------------------------
    UNION ALL SELECT 'Hemidesmus indicus','Indian Sarsaparilla','en','common_name'
    UNION ALL SELECT 'Hemidesmus indicus','Sariva','en','classical_name'
    UNION ALL SELECT 'Hemidesmus indicus','अनंतमूल','hi','common_name'
    UNION ALL SELECT 'Hemidesmus indicus','उटी','mr','common_name'

    --------------------------------------------------------------------
    -- 80. Argyreia speciosa – Vriddhadaru
    --------------------------------------------------------------------
    UNION ALL SELECT 'Argyreia speciosa','Vriddhadaru','en','common_name'
    UNION ALL SELECT 'Argyreia speciosa','Elephant Creeper','en','common_name'
    UNION ALL SELECT 'Argyreia speciosa','वृद्धदारु','hi','common_name'
    UNION ALL SELECT 'Argyreia speciosa','वृद्धदारी','mr','common_name'

    --------------------------------------------------------------------
    -- 81. Bergenia ligulata – Pashanbhed
    --------------------------------------------------------------------
    UNION ALL SELECT 'Bergenia ligulata','Pashanbhed','en','common_name'
    UNION ALL SELECT 'Bergenia ligulata','Stonebreaker Root','en','common_name'
    UNION ALL SELECT 'Bergenia ligulata','पाषाणभेद','hi','common_name'
    UNION ALL SELECT 'Bergenia ligulata','पाषाणभेद','mr','common_name'

    --------------------------------------------------------------------
    -- 82. Mangifera indica – Mango
    --------------------------------------------------------------------
    UNION ALL SELECT 'Mangifera indica','Mango','en','common_name'
    UNION ALL SELECT 'Mangifera indica','Aam','en','common_name'
    UNION ALL SELECT 'Mangifera indica','आम','hi','common_name'
    UNION ALL SELECT 'Mangifera indica','आंबा','mr','common_name'

    --------------------------------------------------------------------
    -- 83. Psoralea corylifolia – Bakuchi
    --------------------------------------------------------------------
    UNION ALL SELECT 'Psoralea corylifolia','Bakuchi','en','common_name'
    UNION ALL SELECT 'Psoralea corylifolia','Babchi','en','common_name'
    UNION ALL SELECT 'Psoralea corylifolia','बाबची','hi','common_name'
    UNION ALL SELECT 'Psoralea corylifolia','बावची','mr','common_name'

    --------------------------------------------------------------------
    -- 84. Acorus calamus – Sweet Flag / Vacha
    --------------------------------------------------------------------
    UNION ALL SELECT 'Acorus calamus','Sweet Flag','en','common_name'
    UNION ALL SELECT 'Acorus calamus','Vacha','en','classical_name'
    UNION ALL SELECT 'Acorus calamus','वचा','hi','common_name'
    UNION ALL SELECT 'Acorus calamus','वच्या','mr','common_name'

    --------------------------------------------------------------------
    -- 85. Piper betle – Betel Leaf
    --------------------------------------------------------------------
    UNION ALL SELECT 'Piper betle','Betel Leaf','en','common_name'
    UNION ALL SELECT 'Piper betle','Pan Leaf','en','common_name'
    UNION ALL SELECT 'Piper betle','पान','hi','common_name'
    UNION ALL SELECT 'Piper betle','पान','mr','common_name'

    --------------------------------------------------------------------
    -- 86. Cinnamomum tamala – Indian Bay Leaf / Tejpatra
    --------------------------------------------------------------------
    UNION ALL SELECT 'Cinnamomum tamala','Indian Bay Leaf','en','common_name'
    UNION ALL SELECT 'Cinnamomum tamala','Tejpatra','en','common_name'
    UNION ALL SELECT 'Cinnamomum tamala','तेजपत्ता','hi','common_name'
    UNION ALL SELECT 'Cinnamomum tamala','तमालपत्र','mr','common_name'

    --------------------------------------------------------------------
    -- 87. Hibiscus rosa-sinensis – Hibiscus
    --------------------------------------------------------------------
    UNION ALL SELECT 'Hibiscus rosa-sinensis','Hibiscus','en','common_name'
    UNION ALL SELECT 'Hibiscus rosa-sinensis','Jaswand','en','common_name'
    UNION ALL SELECT 'Hibiscus rosa-sinensis','जास्वंद','hi','common_name'
    UNION ALL SELECT 'Hibiscus rosa-sinensis','जास्वंद','mr','common_name'

    --------------------------------------------------------------------
    -- 88. Argemone mexicana – Mexican Poppy / Swarna Kshiri
    --------------------------------------------------------------------
    UNION ALL SELECT 'Argemone mexicana','Mexican Poppy','en','common_name'
    UNION ALL SELECT 'Argemone mexicana','Swarna Kshiri','en','classical_name'
    UNION ALL SELECT 'Argemone mexicana','पीला धतूरा','hi','common_name'
    UNION ALL SELECT 'Argemone mexicana','पिवळा डाटूरा','mr','common_name'

    --------------------------------------------------------------------
    -- 89. Calotropis procera – Arka
    --------------------------------------------------------------------
    UNION ALL SELECT 'Calotropis procera','Arka','en','common_name'
    UNION ALL SELECT 'Calotropis procera','Sodom Apple','en','common_name'
    UNION ALL SELECT 'Calotropis procera','आक','hi','common_name'
    UNION ALL SELECT 'Calotropis procera','रूई','mr','common_name'

    --------------------------------------------------------------------
    -- 90. Datura metel – Datura
    --------------------------------------------------------------------
    UNION ALL SELECT 'Datura metel','Datura','en','common_name'
    UNION ALL SELECT 'Datura metel','Dhatura','en','common_name'
    UNION ALL SELECT 'Datura metel','धतूरा','hi','common_name'
    UNION ALL SELECT 'Datura metel','धतूरा','mr','common_name'

    --------------------------------------------------------------------
    -- 91. Boerhavia erecta – Erect Boerhavia / Small Punarnava
    --------------------------------------------------------------------
    UNION ALL SELECT 'Boerhavia erecta','Erect Boerhavia','en','common_name'
    UNION ALL SELECT 'Boerhavia erecta','Small Punarnava','en','common_name'
    UNION ALL SELECT 'Boerhavia erecta','छोटी पुनर्नवा','hi','common_name'
    UNION ALL SELECT 'Boerhavia erecta','लहान पुनर्नवा','mr','common_name'

    --------------------------------------------------------------------
    -- 92. Eclipta alba – Bhringraj
    --------------------------------------------------------------------
    UNION ALL SELECT 'Eclipta alba','Bhringraj','en','common_name'
    UNION ALL SELECT 'Eclipta alba','False Daisy','en','common_name'
    UNION ALL SELECT 'Eclipta alba','भृंगराज','hi','common_name'
    UNION ALL SELECT 'Eclipta alba','भृंगराज','mr','common_name'

    --------------------------------------------------------------------
    -- 93. Ocimum gratissimum – Ram Tulsi
    --------------------------------------------------------------------
    UNION ALL SELECT 'Ocimum gratissimum','Ram Tulsi','en','common_name'
    UNION ALL SELECT 'Ocimum gratissimum','Clove Basil','en','common_name'
    UNION ALL SELECT 'Ocimum gratissimum','राम तुलसी','hi','common_name'
    UNION ALL SELECT 'Ocimum gratissimum','राम तुळस','mr','common_name'

    --------------------------------------------------------------------
    -- 94. Ocimum basilicum – Sweet Basil
    --------------------------------------------------------------------
    UNION ALL SELECT 'Ocimum basilicum','Sweet Basil','en','common_name'
    UNION ALL SELECT 'Ocimum basilicum','Babli Tulsi','en','common_name'
    UNION ALL SELECT 'Ocimum basilicum','मीठी तुलसी','hi','common_name'
    UNION ALL SELECT 'Ocimum basilicum','सुईट बेसिल','mr','common_name'

    --------------------------------------------------------------------
    -- 95. Mentha arvensis – Field Mint / Pudina
    --------------------------------------------------------------------
    UNION ALL SELECT 'Mentha arvensis','Field Mint','en','common_name'
    UNION ALL SELECT 'Mentha arvensis','Pudina','en','common_name'
    UNION ALL SELECT 'Mentha arvensis','पुदीना','hi','common_name'
    UNION ALL SELECT 'Mentha arvensis','पुदीना','mr','common_name'

    --------------------------------------------------------------------
    -- 96. Mentha piperita – Peppermint
    --------------------------------------------------------------------
    UNION ALL SELECT 'Mentha piperita','Peppermint','en','common_name'
    UNION ALL SELECT 'Mentha piperita','Peppermint Mint','en','common_name'
    UNION ALL SELECT 'Mentha piperita','पेपरमिंट','hi','common_name'
    UNION ALL SELECT 'Mentha piperita','पेपरमिंट','mr','common_name'

    --------------------------------------------------------------------
    -- 97. Anethum graveolens – Dill / Shepu
    --------------------------------------------------------------------
    UNION ALL SELECT 'Anethum graveolens','Dill','en','common_name'
    UNION ALL SELECT 'Anethum graveolens','Shepu','en','common_name'
    UNION ALL SELECT 'Anethum graveolens','सोआ','hi','common_name'
    UNION ALL SELECT 'Anethum graveolens','शेपू','mr','common_name'

    --------------------------------------------------------------------
    -- 98. Allium sativum – Garlic
    --------------------------------------------------------------------
    UNION ALL SELECT 'Allium sativum','Garlic','en','common_name'
    UNION ALL SELECT 'Allium sativum','Lahsun','en','common_name'
    UNION ALL SELECT 'Allium sativum','लहसुन','hi','common_name'
    UNION ALL SELECT 'Allium sativum','लसूण','mr','common_name'

    --------------------------------------------------------------------
    -- 99. Allium cepa – Onion
    --------------------------------------------------------------------
    UNION ALL SELECT 'Allium cepa','Onion','en','common_name'
    UNION ALL SELECT 'Allium cepa','Pyaaz','en','common_name'
    UNION ALL SELECT 'Allium cepa','प्याज','hi','common_name'
    UNION ALL SELECT 'Allium cepa','कांदा','mr','common_name'

    --------------------------------------------------------------------
    -- 100. Syzygium cumini – Jamun
    --------------------------------------------------------------------
    UNION ALL SELECT 'Syzygium cumini','Jamun','en','common_name'
    UNION ALL SELECT 'Syzygium cumini','Java Plum','en','common_name'
    UNION ALL SELECT 'Syzygium cumini','जामुन','hi','common_name'
    UNION ALL SELECT 'Syzygium cumini','जांभुळ','mr','common_name'
) AS s
ON p.botanical_name = s.botanical_name;

INSERT INTO plant_disease_mapping (
    plant_id,
    disease_id,
    efficacy_level,
    evidence_type,
    mechanism,
    duration_of_use,
    contraindications,
    special_instructions,
    reference_text
)

SELECT p.id, d.id,
       3,
       'traditional',
       'Cinnamon improves glucose handling and insulin sensitivity alongside digestive stimulation.',
       '8–12 weeks with dietary control.',
       'Use cautiously in patients with very high pitta or on multiple hypoglycemic drugs.',
       'Do not exceed moderate spice doses; monitor blood sugar regularly.',
       'Cinnamon/tvak is described in medoroga and prameha contexts and now studied for glycemic support.'
FROM plants p
JOIN diseases d
  ON p.botanical_name = 'Cinnamomum verum'
 AND d.name_en = 'Diabetes Mellitus Type 2'

UNION ALL
-- 33. Cinnamon – Obesity
SELECT p.id, d.id,
       3,
       'traditional',
       'By improving digestion and scraping kapha–meda, cinnamon supports weight management.',
       '8–12 weeks with exercise and diet.',
       'Avoid overuse in strong pitta constitution.',
       'Use as part of low-calorie, kapha-reducing diet.',
       'Tvak is mentioned among medohara and agni-deepana dravyas.'
FROM plants p
JOIN diseases d
  ON p.botanical_name = 'Cinnamomum verum'
 AND d.name_en = 'Obesity'

UNION ALL
-- 34. Clove – Chronic cough
SELECT p.id, d.id,
       3,
       'traditional',
       'Clove acts as local antiseptic and expectorant, easing sore throat and stubborn cough.',
       '1–3 weeks.',
       'Avoid excessive use in gastritis and small children.',
       'Use as lozenge or in decoction with honey.',
       'Lavanga is used in kasa and kantha roga formulations.'
FROM plants p
JOIN diseases d
  ON p.botanical_name = 'Syzygium aromaticum'
 AND d.name_en = 'Chronic Cough and Bronchitis'

UNION ALL
-- 35. Cardamom – Dyspepsia / mild acidity
SELECT p.id, d.id,
       3,
       'traditional',
       'Cardamom soothes the stomach, freshens breath and relieves heaviness after food.',
       '2–6 weeks in functional dyspepsia.',
       'Usually safe; caution only in very cold and weak agni if used alone.',
       'Often combined with other mild spices after meals.',
       'Ela is described as hridya and deepana in digestive complaints.'
FROM plants p
JOIN diseases d
  ON p.botanical_name = 'Elettaria cardamomum'
 AND d.name_en = 'Gastric Ulcer and Hyperacidity'

UNION ALL
-- 36. Fennel – IBS/colic
SELECT p.id, d.id,
       4,
       'traditional',
       'Fennel relaxes intestinal spasms and reduces gas in vata-predominant IBS and colic.',
       '2–8 weeks, especially after meals.',
       'Use cautiously in very low agni with heavy meals.',
       'Commonly taken as post-meal mouth freshener and carminative.',
       'Madhurika/shatapushpa is used traditionally for colic and flatulence.'
FROM plants p
JOIN diseases d
  ON p.botanical_name = 'Foeniculum vulgare'
 AND d.name_en = 'Diarrhea and IBS'

UNION ALL
-- 37. Cumin – IBS
SELECT p.id, d.id,
       3,
       'traditional',
       'Cumin improves digestion and reduces bloating in functional bowel disorders.',
       '2–8 weeks.',
       'Avoid burning sensation cases with high pitta unless balanced with cooling agents.',
       'Used in small quantities in daily cooking and churnas.',
       'Jeeraka is described for agnimandya and post-partum digestive support.'
FROM plants p
JOIN diseases d
  ON p.botanical_name = 'Cuminum cyminum'
 AND d.name_en = 'Diarrhea and IBS'

UNION ALL
-- 38. Coriander – Jaundice
SELECT p.id, d.id,
       3,
       'traditional',
       'Coriander has mild pitta-reducing and diuretic effect used in burning and early jaundice support.',
       '2–4 weeks along with light diet.',
       'Use cautiously in very cold, low-agni states without warming support.',
       'Often used as coriander seed decoction with sugar for burning and pitta complaints.',
       'Dhanya is used in mutrakricchra and pitta-pradhana conditions including kamala support.'
FROM plants p
JOIN diseases d
  ON p.botanical_name = 'Coriandrum sativum'
 AND d.name_en = 'Jaundice'

UNION ALL
-- 39. Ajwain – IBS
SELECT p.id, d.id,
       4,
       'traditional',
       'Ajwain strongly stimulates digestion and relieves gas and cramps in vata-related bowel disturbance.',
       '1–4 weeks in low doses after food.',
       'Avoid in frank ulcer or severe burning.',
       'Use with rock salt or warm water as advised.',
       'Yavani is classic deepana-pachana herb for ama and colic.'
FROM plants p
JOIN diseases d
  ON p.botanical_name = 'Trachyspermum ammi'
 AND d.name_en = 'Diarrhea and IBS'

UNION ALL
-- 40. Fenugreek – Diabetes
SELECT p.id, d.id,
       4,
       'traditional',
       'Fenugreek seeds slow carbohydrate absorption and support glycemic control.',
       '8–12 weeks along with diet and exercise.',
       'Use cautiously in patients on strong hypoglycemic drugs; monitor sugars.',
       'Prefer soaked or lightly roasted seeds in small divided doses.',
       'Methi is widely used in prameha and medoroga management.'
FROM plants p
JOIN diseases d
  ON p.botanical_name = 'Trigonella foenum-graecum'
 AND d.name_en = 'Diabetes Mellitus Type 2'

UNION ALL
-- 40. Fenugreek – Obesity
SELECT p.id, d.id,
       3,
       'traditional',
       'Fenugreek increases satiety and improves lipid profile supporting weight management.',
       '8–12 weeks.',
       'Avoid large quantities in pregnancy unless supervised.',
       'Use as dietary adjunct in low-calorie regimen.',
       'Fenugreek is used in medoroga and dyslipidemia in integrative practice.'
FROM plants p
JOIN diseases d
  ON p.botanical_name = 'Trigonella foenum-graecum'
 AND d.name_en = 'Obesity'

UNION ALL
-- 41. Black Seed – Asthma
SELECT p.id, d.id,
       3,
       'traditional',
       'Black seed has bronchodilatory and anti-inflammatory effects helpful in asthma.',
       '4–12 weeks with standard therapy.',
       'Not a replacement for inhalers; caution in pregnancy.',
       'Use in small divided doses; monitor respiratory status.',
       'Nigella is used in Unani and regional Ayurveda for shwasa and prameha.'
FROM plants p
JOIN diseases d
  ON p.botanical_name = 'Nigella sativa'
 AND d.name_en = 'Bronchial Asthma'

UNION ALL
-- 41. Black Seed – Diabetes
SELECT p.id, d.id,
       3,
       'traditional',
       'Black seed may improve insulin sensitivity and glucose metabolism.',
       '8–12 weeks.',
       'Monitor sugars when combined with other antidiabetic drugs.',
       'Use as adjunct along with diet control.',
       'Black cumin is used for prameha and metabolic complaints in traditional systems.'
FROM plants p
JOIN diseases d
  ON p.botanical_name = 'Nigella sativa'
 AND d.name_en = 'Diabetes Mellitus Type 2'

UNION ALL
-- 44. Vetiver – Jaundice / burning
SELECT p.id, d.id,
       3,
       'traditional',
       'Vetiver root cools pitta and supports urinary and hepatic function.',
       '2–4 weeks as infusion or decoction.',
       'Use carefully in very cold, low-agni patients.',
       'Often combined with other pitta-pacifying herbs in jwara and daha.',
       'Ushira is mentioned for daha, raktapitta and pitta-related heat states including early kamala.'
FROM plants p
JOIN diseases d
  ON p.botanical_name = 'Chrysopogon zizanioides'
 AND d.name_en = 'Jaundice'

UNION ALL
-- 45. Sandalwood – Chronic Skin Disease
SELECT p.id, d.id,
       4,
       'traditional',
       'Sandalwood heartwood has cooling, anti-inflammatory effect on skin and blood.',
       '4–12 weeks externally and internally as per indication.',
       'Avoid in severe allergy to fragrant woods.',
       'Frequently used as paste or in medicated ghee for skin and pitta disorders.',
       'Chandana is classical raktaprasadana and kushthaghna agent.'
FROM plants p
JOIN diseases d
  ON p.botanical_name = 'Santalum album'
 AND d.name_en = 'Chronic Skin Disease'

UNION ALL
-- 45. Sandalwood – Anxiety and Stress
SELECT p.id, d.id,
       3,
       'traditional',
       'Sandalwood aroma calms mind and supports sattva, reducing mental heat and irritability.',
       '2–8 weeks in mild anxiety and restlessness.',
       'Use cautiously in individuals with fragrance sensitivity.',
       'Used in dhupa, chandan tilaka and medicated oils for manas balancing.',
       'Chandana is noted as hridya and manasashamaka in pitta and rajas-predominant states.'
FROM plants p
JOIN diseases d
  ON p.botanical_name = 'Santalum album'
 AND d.name_en = 'Anxiety and Stress'

UNION ALL
-- 48. Peepal – Cough/bronchitis
SELECT p.id, d.id,
       3,
       'traditional',
       'Peepal bark and leaves help reduce cough and soothe inflamed airways.',
       '2–4 weeks as decoction.',
       'Use cautiously in very weak patients.',
       'Often combined with other shwasahara herbs.',
       'Ashvattha is mentioned in respiratory and bleeding disorders in classics.'
FROM plants p
JOIN diseases d
  ON p.botanical_name = 'Ficus religiosa'
 AND d.name_en = 'Chronic Cough and Bronchitis'

UNION ALL
-- 49. Banyan – Diabetes
SELECT p.id, d.id,
       3,
       'traditional',
       'Banyan bark and aerial roots are used traditionally in formulations for prameha and blood sugar regulation.',
       '8–12 weeks.',
       'Monitor sugars when combined with modern antidiabetics.',
       'Used in decoctions and churnas as prameha-support.',
       'Vata vriksha is described in some nighantus as pramehaghna.'
FROM plants p
JOIN diseases d
  ON p.botanical_name = 'Ficus benghalensis'
 AND d.name_en = 'Diabetes Mellitus Type 2'

UNION ALL
-- 50. Cluster Fig – Diarrhea / IBS
SELECT p.id, d.id,
       4,
       'traditional',
       'Cluster fig bark and fruit act as grahi and astringent in chronic diarrhea.',
       '1–4 weeks.',
       'Avoid in marked constipation.',
       'Used as decoction in atisara and rakta atisara.',
       'Udumbara is part of Nyagrodhadi group for atisara and raktapitta.'
FROM plants p
JOIN diseases d
  ON p.botanical_name = 'Ficus racemosa'
 AND d.name_en = 'Diarrhea and IBS'

UNION ALL
-- 52. Pomegranate – Chronic Liver Disorder
SELECT p.id, d.id,
       3,
       'traditional',
       'Pomegranate rind and juice support digestion and offer antioxidant support for liver and heart.',
       '6–12 weeks.',
       'Caution in severe constipation with excessive rind use.',
       'Prefer properly ripened fruit juice and moderate rind use.',
       'Dadima is revered as hridya and grahi with benefit in chronic digestive and hepatic weakness.'
FROM plants p
JOIN diseases d
  ON p.botanical_name = 'Punica granatum'
 AND d.name_en = 'Chronic Liver Disorder'

UNION ALL
-- 54. Sesame – Osteoporosis
SELECT p.id, d.id,
       4,
       'traditional',
       'Sesame supports asthi dhatu through calcium and healthy fats, strengthening bone tissue.',
       '3–6 months.',
       'Use carefully in high kapha, obesity and hyperlipidemia without balancing regimen.',
       'Best used roasted or as oil in moderation with exercise.',
       'Tila is classic bone and joint-supportive sneha in Ayurveda.'
FROM plants p
JOIN diseases d
  ON p.botanical_name = 'Sesamum indicum'
 AND d.name_en = 'Osteoporosis and Bone Weakness'

UNION ALL
-- 54. Sesame – Neuromuscular Weakness
SELECT p.id, d.id,
       3,
       'traditional',
       'Sesame oil nourishes nerves and muscles, reducing vata-related stiffness and weakness.',
       '6–12 weeks with internal and external use.',
       'Avoid heavy internal use in kapha-prone and obese patients.',
       'Commonly used in abhyanga and basti therapies.',
       'Tila taila is major sneha for vata vyadhi management.'
FROM plants p
JOIN diseases d
  ON p.botanical_name = 'Sesamum indicum'
 AND d.name_en = 'Neuromuscular Weakness'

UNION ALL
-- 55. Flax – Diabetes
SELECT p.id, d.id,
       3,
       'traditional',
       'Flaxseed mucilage slows glucose absorption and improves lipid profile.',
       '8–12 weeks.',
       'Use cautiously in significant GI obstruction.',
       'Take with plenty of water and dietary monitoring.',
       'Atasi is used in contemporary Ayurveda for prameha and medoroga.'
FROM plants p
JOIN diseases d
  ON p.botanical_name = 'Linum usitatissimum'
 AND d.name_en = 'Diabetes Mellitus Type 2'

UNION ALL
-- 55. Flax – Ischemic Heart Disease
SELECT p.id, d.id,
       3,
       'traditional',
       'Omega-rich flax supports healthy lipids and vascular function.',
       '3–6 months.',
       'Caution with anticoagulant medication.',
       'Integrate as part of hridya diet under supervision.',
       'Flaxseed is used in heart-protective dietary regimens in integrative practice.'
FROM plants p
JOIN diseases d
  ON p.botanical_name = 'Linum usitatissimum'
 AND d.name_en = 'Ischemic Heart Disease'

UNION ALL
-- 56. Castor – Neuromuscular Weakness (vata vyadhi)
SELECT p.id, d.id,
       3,
       'traditional',
       'Castor oil relieves vata in joints and nerves when used as purgative and in external applications.',
       'Short courses of 1–3 weeks with supervision.',
       'Strong purgative; contraindicated in pregnancy and severe debility.',
       'Only use under experienced supervision with proper samskara.',
       'Eranda is classical dravya in vata vyadhis with virechana karma.'
FROM plants p
JOIN diseases d
  ON p.botanical_name = 'Ricinus communis'
 AND d.name_en = 'Neuromuscular Weakness'

UNION ALL
-- 57. Karanja – Chronic Skin Disease
SELECT p.id, d.id,
       4,
       'traditional',
       'Karanja oil is antipruritic and antimicrobial, useful in chronic itchy skin conditions.',
       '4–12 weeks mainly external use.',
       'Avoid on open deep wounds or in strong sensitivity.',
       'Commonly applied as karanja taila or in combination oils.',
       'Karanja taila is well-known for kushtha and kandu in Ayurvedic practice.'
FROM plants p
JOIN diseases d
  ON p.botanical_name = 'Pongamia pinnata'
 AND d.name_en = 'Chronic Skin Disease'

UNION ALL
-- 58. Curry Leaf – Diabetes
SELECT p.id, d.id,
       3,
       'traditional',
       'Curry leaves improve insulin function and lipid metabolism in early metabolic disorders.',
       '8–12 weeks with diet control.',
       'Use with caution in severe liver disease without supervision.',
       'Take fresh leaves or powder in small daily quantities.',
       'Karnyanimba is used in South Indian traditional practice for prameha and medoroga.'
FROM plants p
JOIN diseases d
  ON p.botanical_name = 'Murraya koenigii'
 AND d.name_en = 'Diabetes Mellitus Type 2'

UNION ALL
-- 59. Henna – Chronic Skin Disease
SELECT p.id, d.id,
       3,
       'traditional',
       'Henna leaves cool inflamed skin and reduce itching and minor infections.',
       '2–8 weeks, mainly external applications.',
       'Internal use not routine in Ayurveda for skin.',
       'Used as paste or decoction for palms, soles and scalp.',
       'Mehendi is referenced in traditional medicine for burning and skin complaints.'
FROM plants p
JOIN diseases d
  ON p.botanical_name = 'Lawsonia inermis'
 AND d.name_en = 'Chronic Skin Disease'

UNION ALL
-- 60. Aloe – Chronic Liver Disorder
SELECT p.id, d.id,
       3,
       'traditional',
       'Aloe gel supports liver and gut mucosa with mild detoxifying effect.',
       '4–8 weeks.',
       'Avoid in pregnancy and severe diarrhea.',
       'Use processed gel in regulated doses.',
       'Ghritkumari is used in some yakrit and kostha-supportive formulations.'
FROM plants p
JOIN diseases d
  ON p.botanical_name = 'Aloe vera'
 AND d.name_en = 'Chronic Liver Disorder'

UNION ALL
-- 60. Aloe – Chronic Skin Disease
SELECT p.id, d.id,
       4,
       'traditional',
       'Topical aloe promotes wound healing and reduces inflammation in chronic skin lesions.',
       '2–12 weeks on affected areas.',
       'Check for rare contact allergy.',
       'Use fresh gel or standardized preparation.',
       'Aloe is widely employed in vrana and chronic dermatoses management.'
FROM plants p
JOIN diseases d
  ON p.botanical_name = 'Aloe vera'
 AND d.name_en = 'Chronic Skin Disease'

UNION ALL
-- 61. Amaltas – Chronic Skin Disease
SELECT p.id, d.id,
       3,
       'traditional',
       'Aragvadha pulp is used as mild laxative and blood purifier which benefits certain skin conditions.',
       '2–6 weeks.',
       'Excess use may cause loose stools.',
       'Often combined with other raktashodhaka herbs.',
       'Aragvadha is mentioned as kushthaghna and mridu virechaka in classics.'
FROM plants p
JOIN diseases d
  ON p.botanical_name = 'Cassia fistula'
 AND d.name_en = 'Chronic Skin Disease'

UNION ALL
-- 62. Kutaja – Diarrhea / IBS
SELECT p.id, d.id,
       5,
       'traditional',
       'Kutaja bark is strongly astringent and antimicrobial, specific for chronic diarrhea and dysentery.',
       '1–4 weeks under supervision.',
       'Avoid in marked constipation.',
       'Used as kwatha, churna or standardized extract.',
       'Kutaja is prime dravya for atisara and pravahika in Ayurveda.'
FROM plants p
JOIN diseases d
  ON p.botanical_name = 'Holarrhena pubescens'
 AND d.name_en = 'Diarrhea and IBS'

UNION ALL
-- 65. Apamarga – Worms
SELECT p.id, d.id,
       3,
       'traditional',
       'Apamarga has scraping and krimighna action useful in intestinal worm infestations.',
       '1–3 weeks with proper dosing.',
       'Avoid unsupervised strong dosing in children.',
       'Typically part of kshara and krimighna yogas.',
       'Apamarga is included among krimighna and lekhan dravyas.'
FROM plants p
JOIN diseases d
  ON p.botanical_name = 'Achyranthes aspera'
 AND d.name_en = 'Intestinal Worm Infestation'

UNION ALL
-- 65. Apamarga – Chronic Skin Disease
SELECT p.id, d.id,
       3,
       'traditional',
       'By scraping kapha and meda, Apamarga supports management of some stubborn skin conditions.',
       '4–8 weeks under supervision.',
       'Strong, tikshna preparations need expert handling.',
       'Used in kshara karma and lepa for arsha and kushtha.',
       'Apamarga features in kshara-sutra and certain skin disease protocols.'
FROM plants p
JOIN diseases d
  ON p.botanical_name = 'Achyranthes aspera'
 AND d.name_en = 'Chronic Skin Disease'

UNION ALL
-- 66. Red Sandalwood – Chronic Skin Disease
SELECT p.id, d.id,
       4,
       'traditional',
       'Red sandalwood cools blood and reduces inflammation and discoloration in chronic skin disorders.',
       '4–12 weeks mainly external and occasional internal use.',
       'Use sustainable sources due to conservation concerns.',
       'Often combined with other raktashodhaka herbs.',
       'Rakta chandana is classical for raktapitta and kushtha.'
FROM plants p
JOIN diseases d
  ON p.botanical_name = 'Pterocarpus santalinus'
 AND d.name_en = 'Chronic Skin Disease'

UNION ALL
-- 67. Patha – Diarrhea / IBS
SELECT p.id, d.id,
       3,
       'traditional',
       'Patha has grahi and antimicrobial effects helpful in diarrhea and IBS-like presentations.',
       '2–4 weeks.',
       'Avoid in pronounced dryness and constipation.',
       'Used with other grahi dravyas in atisara.',
       'Patha is listed for atisara, jwara and urinary disorders.'
FROM plants p
JOIN diseases d
  ON p.botanical_name = 'Cissampelos pareira'
 AND d.name_en = 'Diarrhea and IBS'

UNION ALL
-- 68. Shati – Asthma
SELECT p.id, d.id,
       3,
       'traditional',
       'Shati clears kapha from chest and works as gentle bronchodilator.',
       '2–6 weeks.',
       'Avoid in very dry vata conditions without moistening agents.',
       'Often part of shwasahara churnas.',
       'Shati is mentioned in kasa and shwasa chikitsa.'
FROM plants p
JOIN diseases d
  ON p.botanical_name = 'Hedychium spicatum'
 AND d.name_en = 'Bronchial Asthma'

UNION ALL
-- 68. Shati – Chronic Cough
SELECT p.id, d.id,
       3,
       'traditional',
       'Aromatic Shati reduces thick phlegm and throat congestion in chronic cough.',
       '2–4 weeks.',
       'Use cautiously in strong pitta throat irritation.',
       'Given as churna or decoction with honey.',
       'Shati is used in many kasa formulations in Himalayan practice.'
FROM plants p
JOIN diseases d
  ON p.botanical_name = 'Hedychium spicatum'
 AND d.name_en = 'Chronic Cough and Bronchitis'

UNION ALL
-- 69. Daruharidra – Chronic Skin Disease
SELECT p.id, d.id,
       4,
       'traditional',
       'Daruharidra acts as antimicrobial and blood purifier in skin diseases.',
       '4–12 weeks.',
       'Use with care in very weak patients.',
       'Often combined with neem and other kushthaghna herbs.',
       'Daruharidra is classical kushthaghna and netrya herb in Ayurveda.'
FROM plants p
JOIN diseases d
  ON p.botanical_name = 'Berberis aristata'
 AND d.name_en = 'Chronic Skin Disease'

UNION ALL
-- 69. Daruharidra – Chronic Liver Disorder
SELECT p.id, d.id,
       4,
       'traditional',
       'Bitter Daruharidra supports liver function and bile flow.',
       '4–12 weeks.',
       'Avoid in severe cachexia without supervision.',
       'Use as decoction or standardized extract.',
       'Daruharidra is cited for yakrit vikara and kamala in classics.'
FROM plants p
JOIN diseases d
  ON p.botanical_name = 'Berberis aristata'
 AND d.name_en = 'Chronic Liver Disorder'

UNION ALL
-- 69. Daruharidra – Jaundice
SELECT p.id, d.id,
       4,
       'traditional',
       'Its tikta rasa and cholagogue effect make Daruharidra suitable in jaundice support.',
       '2–6 weeks.',
       'Use under physician guidance in acute hepatitis.',
       'Combine with light pitta-pacifying diet.',
       'Kiratatikta-type bitters including Daruharidra are used in kamala management.'
FROM plants p
JOIN diseases d
  ON p.botanical_name = 'Berberis aristata'
 AND d.name_en = 'Jaundice'

UNION ALL
-- 70. Chirayata – Recurrent Fever
SELECT p.id, d.id,
       5,
       'traditional',
       'Chirayata is a powerful bitter used in recurrent and chronic fevers.',
       '1–4 weeks.',
       'Excess can weaken agni and weight if overused.',
       'Prefer supervised dosage due to intense bitterness.',
       'Kiratatikta is classical remedy for jwara including visama jwara.'
FROM plants p
JOIN diseases d
  ON p.botanical_name = 'Swertia chirayita'
 AND d.name_en = 'Recurrent Fever'

UNION ALL
-- 70. Chirayata – Chronic Liver Disorder
SELECT p.id, d.id,
       4,
       'traditional',
       'Chirayata supports liver detoxification and pitta clearing in chronic hepatic stress.',
       '4–8 weeks.',
       'Monitor nutrition in underweight individuals.',
       'Use as decoction or in compound bitters.',
       'Kiratatikta is used in yakrit and pitta vikara in classical texts.'
FROM plants p
JOIN diseases d
  ON p.botanical_name = 'Swertia chirayita'
 AND d.name_en = 'Chronic Liver Disorder'

UNION ALL
-- 70. Chirayata – Jaundice
SELECT p.id, d.id,
       4,
       'traditional',
       'Strong tikta rasa of Chirayata is used to clear hepatic heat and bile accumulation.',
       '2–6 weeks.',
       'Avoid prolonged unsupervised use.',
       'Combine with appropriate pitta-pacifying ahara.',
       'Kiratatikta is a standard dravya in kamala chikitsa.'
FROM plants p
JOIN diseases d
  ON p.botanical_name = 'Swertia chirayita'
 AND d.name_en = 'Jaundice'

UNION ALL
-- 71. Galangal – Asthma
SELECT p.id, d.id,
       3,
       'traditional',
       'Galangal warms the chest and reduces kapha obstruction in bronchi.',
       '2–6 weeks.',
       'Use cautiously in strong pitta.',
       'Often combined with other shwasahara spices.',
       'Kulanjana is used for swarabhanga and shwasa in classical practice.'
FROM plants p
JOIN diseases d
  ON p.botanical_name = 'Alpinia galanga'
 AND d.name_en = 'Bronchial Asthma'

UNION ALL
-- 71. Galangal – Chronic Cough
SELECT p.id, d.id,
       3,
       'traditional',
       'Galangal acts as expectorant and throat stimulant improving chronic kapha cough.',
       '2–4 weeks.',
       'Avoid in burning throat.',
       'Given as churna with honey or warm water.',
       'Galangal appears in throat and cough formulas in traditional medicine.'
FROM plants p
JOIN diseases d
  ON p.botanical_name = 'Alpinia galanga'
 AND d.name_en = 'Chronic Cough and Bronchitis'

UNION ALL
-- 72. Nagarmotha (Scariosus) – IBS/diarrhea
SELECT p.id, d.id,
       3,
       'traditional',
       'Nagarmotha cools pitta and improves digestion, helping loose stools and IBS with heat and mucus.',
       '2–4 weeks.',
       'Avoid in severe dryness and constipation.',
       'Used similarly to mustaka in atisara and grahani.',
       'Nagaramusthi is listed for atisara and daha conditions.'
FROM plants p
JOIN diseases d
  ON p.botanical_name = 'Cyperus scariosus'
 AND d.name_en = 'Diarrhea and IBS'

UNION ALL
-- 73. Talispatra – Asthma
SELECT p.id, d.id,
       3,
       'traditional',
       'Talispatra clears kapha from chest and eases breathing in asthma.',
       '2–6 weeks.',
       'Avoid very high pitta conditions.',
       'Given as churna or decoction with honey.',
       'Talisapatra is shwasahara and kasahara in classics.'
FROM plants p
JOIN diseases d
  ON p.botanical_name = 'Abies webbiana'
 AND d.name_en = 'Bronchial Asthma'

UNION ALL
-- 73. Talispatra – Chronic Cough
SELECT p.id, d.id,
       3,
       'traditional',
       'Acts as aromatic expectorant in chronic kapha cough.',
       '2–4 weeks.',
       'Use carefully in strong dryness.',
       'Often combined with sitopaladi-type churnas.',
       'Talispatra is widely used in kasa formulations.'
FROM plants p
JOIN diseases d
  ON p.botanical_name = 'Abies webbiana'
 AND d.name_en = 'Chronic Cough and Bronchitis'

UNION ALL
-- 74. Pushkarmoola – Ischemic Heart Disease
SELECT p.id, d.id,
       4,
       'traditional',
       'Pushkarmoola acts as hridya, improving coronary circulation and relieving chest discomfort.',
       '4–12 weeks with medical supervision.',
       'Not a substitute for emergency cardiac care.',
       'Use in small doses under physician guidance.',
       'Pushkarmoola is classical hridya dravya for hridroga.'
FROM plants p
JOIN diseases d
  ON p.botanical_name = 'Inula racemosa'
 AND d.name_en = 'Ischemic Heart Disease'

UNION ALL
-- 75. Black Nightshade – Liver
SELECT p.id, d.id,
       3,
       'traditional',
       'Black nightshade reduces hepatic inflammation and supports detoxification.',
       '4–8 weeks.',
       'Use processed and correct species; avoid toxic misidentification.',
       'Given as leafy preparation or decoction.',
       'Kakamachi is used in yakrit vikara and pittaja conditions.'
FROM plants p
JOIN diseases d
  ON p.botanical_name = 'Solanum nigrum'
 AND d.name_en = 'Chronic Liver Disorder'

UNION ALL
-- 76. Vidarikand – Diabetes / weakness
SELECT p.id, d.id,
       3,
       'traditional',
       'Vidarikand nourishes depleted tissues and supports metabolism in prameha with weakness.',
       '8–12 weeks.',
       'May increase kapha and weight if used excessively.',
       'Use with monitored diet in diabetics.',
       'Vidarikanda is shukra and balya rasayana used in prameha-associated debility.'
FROM plants p
JOIN diseases d
  ON p.botanical_name = 'Pueraria tuberosa'
 AND d.name_en = 'Diabetes Mellitus Type 2'

UNION ALL
-- 78. Kalijiri – Worms
SELECT p.id, d.id,
       4,
       'traditional',
       'Kalijiri has strong krimighna and digestive stimulant action helpful in intestinal worms.',
       '1–3 weeks.',
       'Avoid high doses without supervision.',
       'Best used in combination with other krimighna herbs.',
       'Kalijiri is used for krimi and skin conditions in traditional practice.'
FROM plants p
JOIN diseases d
  ON p.botanical_name = 'Centratherum anthelminticum'
 AND d.name_en = 'Intestinal Worm Infestation'

UNION ALL
-- 78. Kalijiri – Chronic Skin Disease
SELECT p.id, d.id,
       3,
       'traditional',
       'By clearing internal toxins and worms, Kalijiri indirectly supports chronic skin disease management.',
       '4–8 weeks as part of formulations.',
       'Not used as sole long-term agent.',
       'Used in raktashodhaka and krimighna blends.',
       'Traditional use links Kalijiri to krimi and kushtha management.'
FROM plants p
JOIN diseases d
  ON p.botanical_name = 'Centratherum anthelminticum'
 AND d.name_en = 'Chronic Skin Disease'

UNION ALL
-- 79. Sariva – Chronic Skin Disease
SELECT p.id, d.id,
       4,
       'traditional',
       'Sariva cools blood and clears pitta, very useful in chronic itching and rashes.',
       '8–16 weeks.',
       'Generally safe; monitor in very cold prakriti.',
       'Given as decoction, syrup or ghee.',
       'Sariva is prime raktashodhaka dravya for kushtha and raktapitta.'
FROM plants p
JOIN diseases d
  ON p.botanical_name = 'Hemidesmus indicus'
 AND d.name_en = 'Chronic Skin Disease'

UNION ALL
-- 79. Sariva – Jaundice
SELECT p.id, d.id,
       3,
       'traditional',
       'Its pitta pacifying effect supports management of jaundice with itching and heat.',
       '4–8 weeks.',
       'Use with other hepatic bitters for better effect.',
       'Often combined with other raktashodhaka herbs in kamala.',
       'Sariva is used in pitta and rakta vikaras including kamala.'
FROM plants p
JOIN diseases d
  ON p.botanical_name = 'Hemidesmus indicus'
 AND d.name_en = 'Jaundice'

UNION ALL
-- 80. Vriddhadaru – Neuromuscular Weakness
SELECT p.id, d.id,
       3,
       'traditional',
       'Vriddhadaru strengthens muscles and nerves as balya and rasayana.',
       '8–16 weeks.',
       'May increase kapha if overused without activity.',
       'Use with appropriate physiotherapy or exercise.',
       'Vriddhadaru is noted for vata vyadhi and neuromuscular weakness in texts.'
FROM plants p
JOIN diseases d
  ON p.botanical_name = 'Argyreia speciosa'
 AND d.name_en = 'Neuromuscular Weakness'

UNION ALL
-- 81. Pashanbhed – Urinary Stones
SELECT p.id, d.id,
       5,
       'traditional',
       'Pashanbhed exerts antiurolithic action and eases passage of urinary stones.',
       '4–12 weeks with adequate hydration.',
       'Not a substitute for emergency management of obstructive stones.',
       'Use under medical supervision when stones are present.',
       'Pashanbheda is classical dravya for ashmari and mutrakricchra.'
FROM plants p
JOIN diseases d
  ON p.botanical_name = 'Bergenia ligulata'
 AND d.name_en = 'Urinary Stones'

UNION ALL
-- 83. Bakuchi – Chronic Skin Disease
SELECT p.id, d.id,
       5,
       'traditional',
       'Bakuchi stimulates pigment production and treats vitiligo and other chronic skin disorders.',
       '3–6 months under strict supervision.',
       'Photosensitivity and hepatic risk with improper dosing.',
       'Requires precise dosing, often with sun exposure guidance.',
       'Bakuchi is central dravya in shwitra (vitiligo) chikitsa.'
FROM plants p
JOIN diseases d
  ON p.botanical_name = 'Psoralea corylifolia'
 AND d.name_en = 'Chronic Skin Disease'

UNION ALL
-- 84. Vacha – Anxiety and Stress
SELECT p.id, d.id,
       3,
       'traditional',
       'Vacha clears kapha from head and enhances clarity of mind, reducing mental dullness and some anxiety states.',
       '2–8 weeks.',
       'High doses may be too stimulating or irritant.',
       'Use in very small quantity in churna or ghee under guidance.',
       'Vacha is medhya and used in manas and speech disorders.'
FROM plants p
JOIN diseases d
  ON p.botanical_name = 'Acorus calamus'
 AND d.name_en = 'Anxiety and Stress'

UNION ALL
-- 84. Vacha – Memory Weakness
SELECT p.id, d.id,
       3,
       'traditional',
       'By improving clarity and circulation to head, Vacha supports memory and learning.',
       '4–8 weeks.',
       'Use in minute doses only.',
       'Often combined with other medhya herbs.',
       'Vacha features among medhya rasayana dravyas.'
FROM plants p
JOIN diseases d
  ON p.botanical_name = 'Acorus calamus'
 AND d.name_en = 'Memory Weakness'

UNION ALL
-- 84. Vacha – Chronic Cough
SELECT p.id, d.id,
       3,
       'traditional',
       'Vacha helps expel sticky kapha from upper respiratory tract.',
       '2–4 weeks.',
       'Avoid in strong pitta throat burning.',
       'Usually given with honey as anupana.',
       'Vacha is shirovirechana and kasahara in texts.'
FROM plants p
JOIN diseases d
  ON p.botanical_name = 'Acorus calamus'
 AND d.name_en = 'Chronic Cough and Bronchitis'

UNION ALL
-- 87. Hibiscus – Menstrual Irregularity
SELECT p.id, d.id,
       3,
       'traditional',
       'Hibiscus flowers support menstrual balance and reduce excessive heat and pitta in cycle.',
       '2–6 cycles.',
       'Use cautiously in heavy uncontrolled bleeding; seek medical evaluation.',
       'Commonly used as tea or decoction for menstrual support.',
       'Japa pushpa is used for raktapitta and women''s health in traditional practice.'
FROM plants p
JOIN diseases d
  ON p.botanical_name = 'Hibiscus rosa-sinensis'
 AND d.name_en = 'Menstrual Irregularity'

UNION ALL
-- 88. Swarna Kshiri – Chronic Skin Disease
SELECT p.id, d.id,
       3,
       'traditional',
       'Used in minute doses, Swarna kshiri is applied in some stubborn skin conditions.',
       'Short supervised courses only.',
       'Plant is toxic; strict professional guidance mandatory.',
       'Never self-medicate with this herb.',
       'Swarna kshiri is mentioned with caution for kushtha in some nighantus.'
FROM plants p
JOIN diseases d
  ON p.botanical_name = 'Argemone mexicana'
 AND d.name_en = 'Chronic Skin Disease'

UNION ALL
-- 89. Arka – Chronic Skin Disease
SELECT p.id, d.id,
       3,
       'traditional',
       'Arka latex is used externally as counter-irritant and in some skin conditions.',
       'Short-term local application only.',
       'Highly irritant and potentially toxic; must be diluted and supervised.',
       'Avoid near eyes and mucosa.',
       'Arka appears in kshara and external therapies for arsha and selected skin lesions.'
FROM plants p
JOIN diseases d
  ON p.botanical_name = 'Calotropis procera'
 AND d.name_en = 'Chronic Skin Disease'

UNION ALL
-- 90. Datura – Asthma
SELECT p.id, d.id,
       3,
       'traditional',
       'Processed Datura leaf and seed provide bronchodilation and relieve wheeze in asthma.',
       'Short, strictly supervised courses.',
       'Highly toxic if misused; narrow safety margin.',
       'Used only after proper shodhana by experts, often as fumigation or small internal dose.',
       'Dhattura is described in shwasa roga with stringent processing rules.'
FROM plants p
JOIN diseases d
  ON p.botanical_name = 'Datura metel'
 AND d.name_en = 'Bronchial Asthma'

UNION ALL
-- 92. Bhringraj – Chronic Liver Disorder
SELECT p.id, d.id,
       4,
       'traditional',
       'Bhringraj supports liver regeneration and bile flow.',
       '4–12 weeks.',
       'Monitor liver parameters in serious disease.',
       'Used as juice, decoction or taila.',
       'Bhringaraja is mentioned in yakrit vikara and as rasayana for liver and hair.'
FROM plants p
JOIN diseases d
  ON p.botanical_name = 'Eclipta alba'
 AND d.name_en = 'Chronic Liver Disorder'

UNION ALL
-- 92. Bhringraj – Chronic Skin Disease
SELECT p.id, d.id,
       3,
       'traditional',
       'By supporting liver and raktadhatu, Bhringraj aids some chronic skin issues.',
       '8–16 weeks.',
       'Check for plant allergy.',
       'Often used as taila on scalp and skin.',
       'Bhringaraja taila is classic keshya and skin-supportive oil.'
FROM plants p
JOIN diseases d
  ON p.botanical_name = 'Eclipta alba'
 AND d.name_en = 'Chronic Skin Disease'

UNION ALL
-- 93. Ram Tulsi – Cough and Asthma
SELECT p.id, d.id,
       4,
       'traditional',
       'Ram Tulsi acts as expectorant and bronchodilator improving cough and mild asthma.',
       '2–8 weeks.',
       'Avoid in very high pitta without balancing.',
       'Use as fresh leaf juice or tea with honey.',
       'Tulsi variants are shwasahara and kasahara in Ayurveda.'
FROM plants p
JOIN diseases d
  ON p.botanical_name = 'Ocimum gratissimum'
 AND d.name_en = 'Chronic Cough and Bronchitis'

UNION ALL
SELECT p.id, d.id,
       3,
       'traditional',
       'Same herb relieves bronchospasm and congestion in bronchi.',
       '2–8 weeks.',
       'Not a replacement for inhalers in acute attacks.',
       'Use as adjunct with prescribed modern care.',
       'Tulsi is widely recognized for shwasa in classics and folk practice.'
FROM plants p
JOIN diseases d
  ON p.botanical_name = 'Ocimum gratissimum'
 AND d.name_en = 'Bronchial Asthma'

UNION ALL
-- 95. Field Mint – IBS / dyspepsia
SELECT p.id, d.id,
       3,
       'traditional',
       'Field mint relaxes gut smooth muscle and reduces gas and nausea.',
       '2–8 weeks.',
       'Excess may aggravate very cold vata conditions.',
       'Given as chutney, tea or in syrups.',
       'Pudina is widely used in Ayurvedic-style digestive remedies.'
FROM plants p
JOIN diseases d
  ON p.botanical_name = 'Mentha arvensis'
 AND d.name_en = 'Diarrhea and IBS'

UNION ALL
-- 96. Peppermint – IBS
SELECT p.id, d.id,
       4,
       'traditional',
       'Peppermint oil has antispasmodic effect and helps IBS with crampy pain.',
       '4–12 weeks.',
       'Use enteric-coated forms and avoid reflux-prone patients without supervision.',
       'Dose and quality must be regulated.',
       'Peppermint is a recognized antispasmodic in modern herbal gastroenterology.'
FROM plants p
JOIN diseases d
  ON p.botanical_name = 'Mentha piperita'
 AND d.name_en = 'Diarrhea and IBS'

UNION ALL
-- 97. Dill – Infantile colic / IBS
SELECT p.id, d.id,
       4,
       'traditional',
       'Dill seed reduces colic and gas especially in infants and nursing mothers.',
       '2–6 weeks in small doses.',
       'Use carefully in infants; dose must be tiny and supervised.',
       'Often used as water or mild decoction.',
       'Shatapushpa is classic for bal colic and stanya vriddhi.'
FROM plants p
JOIN diseases d
  ON p.botanical_name = 'Anethum graveolens'
 AND d.name_en = 'Diarrhea and IBS'

UNION ALL
-- 98. Garlic – Ischemic Heart Disease
SELECT p.id, d.id,
       4,
       'traditional',
       'Garlic improves lipid profile, reduces platelet aggregation and supports vascular health.',
       '3–6 months.',
       'Caution with anticoagulant drugs and pre-surgery.',
       'Use in moderate daily dietary doses.',
       'Lashuna is described for medoroga, shotha and hridroga in texts and modern studies.'
FROM plants p
JOIN diseases d
  ON p.botanical_name = 'Allium sativum'
 AND d.name_en = 'Ischemic Heart Disease'

UNION ALL
-- 98. Garlic – Diabetes / Obesity
SELECT p.id, d.id,
       3,
       'traditional',
       'Garlic supports glucose and lipid metabolism in metabolic syndrome.',
       '8–12 weeks.',
       'Watch for gastric irritation in some patients.',
       'Best used cooked or mildly raw with food.',
       'Garlic is used in medoroga and prameha-supportive dietary regimens.'
FROM plants p
JOIN diseases d
  ON p.botanical_name = 'Allium sativum'
 AND d.name_en = 'Diabetes Mellitus Type 2'

UNION ALL
SELECT p.id, d.id,
       3,
       'traditional',
       'Its scraping effect on meda helps in obesity programs along with exercise.',
       '8–16 weeks.',
       'Avoid overuse in pitta prakriti.',
       'Integrate with lifestyle measures.',
       'Deepana and medohara properties are highlighted in traditional use.'
FROM plants p
JOIN diseases d
  ON p.botanical_name = 'Allium sativum'
 AND d.name_en = 'Obesity'

UNION ALL
-- 99. Onion – Diabetes
SELECT p.id, d.id,
       3,
       'traditional',
       'Onion may improve insulin sensitivity and lipids as part of diet.',
       '3–6 months.',
       'Consider digestive tolerance in some individuals.',
       'Use as regular vegetable in balanced amount.',
       'Palandu is mentioned with hridya and deepana qualities that align with metabolic support.'
FROM plants p
JOIN diseases d
  ON p.botanical_name = 'Allium cepa'
 AND d.name_en = 'Diabetes Mellitus Type 2'

UNION ALL
-- 99. Onion – Ischemic Heart Disease
SELECT p.id, d.id,
       3,
       'traditional',
       'Onion provides antioxidant and mild antiplatelet support beneficial in heart health.',
       '3–6 months.',
       'Caution with anticoagulant medications.',
       'Use in cooked form as regular part of hridya diet.',
       'Onion is used traditionally as heart-supportive and circulation-supportive food.'
FROM plants p
JOIN diseases d
  ON p.botanical_name = 'Allium cepa'
 AND d.name_en = 'Ischemic Heart Disease'

UNION ALL
-- 100. Jamun – Diabetes
SELECT p.id, d.id,
       5,
       'traditional',
       'Jamun seed powder improves glycemic control and insulin function in Type 2 diabetes.',
       '8–16 weeks with monitoring.',
       'Adjust if patient already on strong antidiabetic medication.',
       'Use standardized seed powder in regulated dose.',
       'Jambu seeds are classic in prameha chikitsa in Ayurveda.'
FROM plants p
JOIN diseases d
  ON p.botanical_name = 'Syzygium cumini'
 AND d.name_en = 'Diabetes Mellitus Type 2'
;
