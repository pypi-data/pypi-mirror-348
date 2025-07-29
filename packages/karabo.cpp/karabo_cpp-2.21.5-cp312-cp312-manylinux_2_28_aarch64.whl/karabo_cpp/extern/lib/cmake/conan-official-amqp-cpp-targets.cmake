if(TARGET amqpcpp::amqpcpp AND NOT TARGET amqpcpp)
    add_library(amqpcpp INTERFACE IMPORTED)
    set_property(TARGET amqpcpp PROPERTY INTERFACE_LINK_LIBRARIES amqpcpp::amqpcpp)
endif()
