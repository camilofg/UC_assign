import sys
import adjusts_tramos_file as atf

if sys.argv[1] is not None:
    print(sys.argv[0])
    xml_config = sys.argv[1]
    print(xml_config)
    try:
        test = atf.AdjustsTramosFile(xml_config)
        test.start_clean_file()
    except Exception as err:
        print(err)

    #text = input('test: ')
