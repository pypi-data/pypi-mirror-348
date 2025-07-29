from wowool.io.console.argument_parser import ArgumentParser as ArgumentParserBase


# fmt: off
class ArgumentParser(ArgumentParserBase):

    def __init__(self):
        """
            Configuration example that you can add the to dom_info file or pass it to the configuration.
            "themes" : {
            "collect" : {
                "Person": { "uri" : false , "attributes" : [ "gender" ]},
                "Company": { "uri" : true }
        },
        "attributes" : [ "sector" , "theme" ]
        }
        You need a section 'themes' in this section you need a section 'collect' which will describe what you want to collect.
        - uri collect the uri name.
        - attributes to collect for the given concept uri.
        In the toplevel dict the 'attributes' keyword is the set of attributes you want to collect on all concepts.
        """

        super(ArgumentParserBase, self).__init__(prog="themes", description=ArgumentParser.__call__.__doc__)
        self.add_argument("-p", "--pipeline", help="pipeline to process." "")
        self.add_argument("--config", help="the themes json config file.")
        self.add_argument("-f", "--file", help="folder or file you want to process")
        self.add_argument("-i", "--text", help="the string you want to process")
        self.add_argument("--debug", help="verbose info", default=False, action="store_true")
        self.add_argument("--json", help="verbose output", default=False, action="store_true")
        self.add_argument("--raw_print", help="print nicely", default=False, action="store_true")
        self.add_argument("-c", "--count", help="count of desired themes", type=int, default=5)
        self.add_argument("-t", "--threshold", help="threshold of desired themes [0-100]", type=int, default=0)

# fmt: on
