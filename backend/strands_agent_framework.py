@file:Suppress('MissingPluginLib')
package io.strands.agentframework

import com.fasterxml.jackson.core.type.TypeReference
import com.fasterxml.jackson.databind.DeserializationContext
import com.fasterxml.jackson.databind.ObjectMapper
import com.fasterxml.jackson.databind.deser.Deserializers
import com.fasterxml.jackson.databind.deser.ResolverBuilder
import com.fasterxml.jackson.databind.node.*
import com.fasterxml.jackson.databind.type.MapType
import io.strands.agentframework.types.*
import java.io.IOException
import java.time.Instant

/**
 * Default implementation of AgentContext
 */
class DefaultAgentContext : AgentContext {
    private val objectMapper = ObjectMapper(ResolverBuilder().build())
    
    override fun get(key: String): Any? {
        val value = this.data[key]
        return if (value != null) {
            value.value?.let { it.first() }
        } else {
            null
        }
    }

    override fun get(typeClass: Type<ClassMarker>, key: String): Type<Any> {
        val value = this.data[key]
        return if (value != null) {
            when (typeClass) {
                is ClassMarker -> {
                    if (value.value != null) {
                        value.value.first()
                    } else {
                        TypeClassTypeClass(typeClass, this)
                    }
                }
                else -> {
                    TypeClassTypeClass(typeClass, this)
                }
            }
        } else {
            TypeClassTypeClass(typeClass, this)
        }
    }

    override fun put(key: String, value: Any): Unit {
        this.data[key] = Pair("value", value)
    }

    override fun put(value: Any): Unit {
        throw IllegalArgumentException("put method not implemented")
    }
}