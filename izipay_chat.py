import streamlit as st
import requests
import json
from datetime import datetime
from zoneinfo import ZoneInfo

# Zona horaria de Lima, Perú
LIMA_TZ = ZoneInfo("America/Lima")

# Configuración de la página
st.set_page_config(
    page_title="Chat izipay",
    page_icon="🤖",
    layout="wide"
)

# Configuración de la API de Izipay
API_ENDPOINT = "https://dev-chat-izipay-postventa-genai-api-322392286721.us-central1.run.app/bloque2"
API_HEADERS = {
    "Content-Type": "application/json",
    "token": "dev-chatpgt-token-xbpr435"
}

def call_api(message, user_id=None, session_id=None, tematica="app_izipay"):
    """
    Función para llamar a la API de Izipay con diferentes configuraciones según la temática
    """
    try:
        # Configuración base común
        base_config = {
            "question": message,
            "metadata": {
                "userId": user_id,
                "channelType": "Demo-Web",
                "sessionId": session_id
            },
            "configuration": {
                "business_case": "Asistente virtual de Izipay",
                "prompt_params": {
                    "assistant_name": "Izi",
                    "assistant_role": "Actúa como asistente virtual de Izipay",
                    "company_name": "Izipay",
                    "company_activity": "Venta de servicios y terminales de puntos de venta llamados POS para la compra y venta",
                    "conversation_purpose": "Atiende las consultas de los usuarios con entusiasmo y responde siempre de manera clara, breve y precisa. Tu misión principal es brindar soporte sobre todos los productos y servicios de Izipay, especialmente los terminales POS y cualquier otro servicio relacionado.\n- Tono: Siempre animado, profesional y directo.\n- Preguntas ambiguas: Si la pregunta no está clara, pide detalles específicos para poder ofrecer una respuesta adecuada.\n- Límites: Si no puedes resolver algo, redirige al usuario con instrucciones claras para contactar al equipo de soporte humano."
                },
                "config_params": {
                    "maxMinutes": "None",
                    "temperature": 0.3,
                    "k_top_retrieval": 3
                }
            }
        }

        # Configuración específica según la temática
        if tematica == "app_izipay":
            base_config["configuration"]["knowledge_stores"] = ["dev_izipay_apiz_apiz_azureopenai"]
            
        elif tematica == "izipay_ya":
            base_config["configuration"]["knowledge_stores"] = ["dev_izipay_index_izya_azureopenai"]

        elif tematica == "soporte_tecnico":
            base_config["configuration"]["knowledge_stores"] = ["dev_izipay_index_sote_azureopenai"]

        elif tematica == "agente_izipay":
            base_config["configuration"]["knowledge_stores"] = ["dev_izipay_index_agiz_azureopenai"]

        elif tematica == "retiro_inmediato":
            base_config["configuration"]["knowledge_stores"] = ["dev_izipay_index_rein_azureopenai"]

        elif tematica == "arisale":
            base_config["configuration"]["knowledge_stores"] = ["dev_izipay_index_aris_azureopenai"]

        elif tematica == "compra_estatus_pedido":
            base_config["configuration"]["knowledge_stores"] = ["dev_izipay_index_coes_azureopenai"]
        
        elif tematica == "ventas_abonos":
            base_config["configuration"]["knowledge_stores"] = ["dev_izipay_index_veab_azureopenai"]

        elif tematica == "datos_comercio":
            base_config["configuration"]["knowledge_stores"] = ["dev_izipay_index_daco_azureopenai"]

        elif tematica == "productos_virtuales":
            base_config["configuration"]["knowledge_stores"] = ["dev_izipay_index_prvi_azureopenai"]

        elif tematica == "solicitud_contometros":
            base_config["configuration"]["knowledge_stores"] = ["dev_izipay_index_soco_azureopenai"]

        response = requests.post(
            API_ENDPOINT,
            headers=API_HEADERS,
            json=base_config,
            timeout=90
        )

        if response.status_code == 200:
            result = response.json()
            # Extraer la respuesta específica de Izipay
            answer = result.get("answer", "Sin respuesta disponible")

            # Información adicional que se puede mostrar
            trace = result.get("trace", "")
            trace_description = result.get("trace_description", "")
            satisfaction = result.get("satisfaction", "")
            transfer = result.get("transfer", "")
            finish = result.get("finish", "")
            citations = result.get("citations", [])

            return {
                "answer": answer,
                "trace": trace,
                "trace_description": trace_description,
                "citations": citations,
                "satisfaction": satisfaction,
                "transfer": transfer,
                "finish": finish,
                "raw_response": result
            }, None
        else:
            return f"Error API: {response.status_code} - {response.text}", "error"

    except requests.exceptions.RequestException as e:
        return f"Error de conexión: {str(e)}", "error"
    except Exception as e:
        return f"Error inesperado: {str(e)}", "error"

# Inicializar el historial de chat y configuración
if "messages" not in st.session_state:
    st.session_state.messages = []
if "session_id" not in st.session_state:
    st.session_state.session_id = f"SESSION-{datetime.now(LIMA_TZ).strftime('%Y%m%d%H%M%S')}"
if "user_id" not in st.session_state:
    st.session_state.user_id = f"USER-{datetime.now(LIMA_TZ).strftime('%Y%m%d%H%M%S')}"
if "tematica_seleccionada" not in st.session_state:
    st.session_state.tematica_seleccionada = "app_izipay"

# Título de la aplicación
if st.session_state.tematica_seleccionada == "app_izipay":
    tematica_nombre = "App Izipay"
elif st.session_state.tematica_seleccionada == "izipay_ya":
    tematica_nombre = "Izipay YA"
elif st.session_state.tematica_seleccionada == "soporte_tecnico":
    tematica_nombre = "Soporte técnico"
elif st.session_state.tematica_seleccionada == "agente_izipay":
    tematica_nombre = "Agente Izipay"
elif st.session_state.tematica_seleccionada == "retiro_inmediato":
    tematica_nombre = "Retiro Inmediato"
elif st.session_state.tematica_seleccionada == "arisale":
    tematica_nombre = "Arisale"
elif st.session_state.tematica_seleccionada == "compra_estatus_pedido":
    tematica_nombre = "Compra o estatus de mi pedido"
elif st.session_state.tematica_seleccionada == "ventas_abonos":
    tematica_nombre = "Mis ventas y abonos"
elif st.session_state.tematica_seleccionada == "datos_comercio":
    tematica_nombre = "Mis datos de comercio"
elif st.session_state.tematica_seleccionada == "productos_virtuales":
    tematica_nombre = "Otros productos virtuales"
elif st.session_state.tematica_seleccionada == "solicitud_contometros":
    tematica_nombre = "Solicitud de contómetros"
st.title(f"🤖 {tematica_nombre}")

# Sidebar con información
with st.sidebar:
    st.header("Temáticas")
    
    # 1. Definimos un diccionario para mapear el Nombre Visible -> Clave Interna
    # Esto permite usar emojis y textos bonitos sin romper tu lógica interna de API
    MAPA_TEMATICAS = {
        "📱 App Izipay": "app_izipay",
        "🚀 Izipay YA": "izipay_ya",
        "🛠️ Soporte técnico": "soporte_tecnico",
        "🏪 Agente Izipay": "agente_izipay",
        "💸 Retiro inmediato": "retiro_inmediato",
        "💳 Arisale": "arisale",
        "📦 Compra/Estatus pedido": "compra_estatus_pedido",
        "💰 Mis ventas y abonos": "ventas_abonos",
        "🏢 Mis datos de comercio": "datos_comercio",
        "🌐 Productos virtuales": "productos_virtuales",
        "📄 Solicitud contómetros": "solicitud_contometros"
    }

    # 2. Encontramos la opción actual para mantener la selección
    # Buscamos qué llave del diccionario coincide con el estado actual
    current_index = 0
    keys_list = list(MAPA_TEMATICAS.values())
    if st.session_state.tematica_seleccionada in keys_list:
        current_index = keys_list.index(st.session_state.tematica_seleccionada)

    # 3. El Widget de Selección
    seleccion = st.radio(
        "Selecciona una consulta:",
        options=list(MAPA_TEMATICAS.keys()),
        index=current_index,
        label_visibility="collapsed" # Ocultamos el label para que se vea más limpio
    )

    # 4. Actualizamos el estado automáticamente
    # Si la selección cambia, actualizamos la session_state
    nuevo_valor = MAPA_TEMATICAS[seleccion]
    if st.session_state.tematica_seleccionada != nuevo_valor:
        st.session_state.tematica_seleccionada = nuevo_valor
        st.rerun()

    st.markdown("---")

    # Configuración de usuario y sesión
    st.subheader("⚙️ Gestión de Usuario y Sesión")
    
    # Agrupamos los detalles técnicos en un desplegable para no saturar la vista
    with st.expander("Ver Usuario y Sesión", expanded=False):
        st.caption("Usuario")
        st.text_input("User ID", value=st.session_state.user_id, disabled=True, label_visibility="collapsed")
        
        st.caption("Sesión")
        st.text_input("Session ID", value=st.session_state.session_id, disabled=True, label_visibility="collapsed")

    # Acciones principales separadas para fácil acceso
    col_actions_1, col_actions_2 = st.columns(2)
    
    with col_actions_1:
        if st.button("👤 Nuevo Usuario", help="Reinicia identidad y chat", use_container_width=True):
            st.session_state.user_id = f"USER-{datetime.now(LIMA_TZ).strftime('%Y%m%d%H%M%S')}"
            st.session_state.messages = []
            st.session_state.session_id = f"SESSION-{datetime.now(LIMA_TZ).strftime('%Y%m%d%H%M%S')}"
            st.rerun()
            
    with col_actions_2:
        if st.button("💬 Nueva Sesión", help="Mantiene usuario, reinicia chat", use_container_width=True):
            st.session_state.session_id = f"SESSION-{datetime.now(LIMA_TZ).strftime('%Y%m%d%H%M%S')}"
            st.rerun()
            
    st.markdown("---")
    
    # Botón de limpieza destacado
    if st.button("🗑️ Limpiar Historial", use_container_width=True, type="primary"):
        st.session_state.messages = []
        st.session_state.session_id = f"SESSION-{datetime.now(LIMA_TZ).strftime('%Y%m%d%H%M%S')}"
        st.rerun()

# Contenedor para el chat
chat_container = st.container()

# Mostrar historial de mensajes
with chat_container:
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            if message.get("timestamp"):
                st.caption(f"🕐 {message['timestamp']}")

# Input para nuevo mensaje
if prompt := st.chat_input("Escribe tu mensaje aquí..."):
    # Agregar mensaje del usuario al historial
    timestamp = datetime.now(LIMA_TZ).strftime("%H:%M")
    st.session_state.messages.append({
        "role": "user",
        "content": prompt,
        "timestamp": timestamp
    })
    
    # Mostrar mensaje del usuario
    with st.chat_message("user"):
        st.markdown(prompt)
        st.caption(f"🕐 {timestamp}")
    
    # Llamar a la API y mostrar respuesta
    with st.chat_message("assistant"):
        with st.spinner("Respondiendo..."):
            response_data, error = call_api(
                prompt, 
                st.session_state.user_id, 
                st.session_state.session_id,
                st.session_state.tematica_seleccionada
            )

            if error:
                st.error(response_data)
                response_text = "Lo siento, ocurrió un error al procesar tu mensaje."
                response_info = None
            else:
                response_text = response_data["answer"]
                response_info = response_data

            st.markdown(response_text)
            response_timestamp = datetime.now(LIMA_TZ).strftime("%H:%M")
            st.caption(f"🕐 {response_timestamp}")

            # Mostrar información adicional si está disponible
            if response_info and response_info.get("trace_description"):
                with st.expander("📋 Información adicional"):
                    if response_info.get("trace"):
                        st.write(f"**Traza:** {response_info['trace']}")
                    st.write(f"**Descripción de la traza:** {response_info['trace_description']}")
                    st.write(f"**Satisfacción:** {response_info['satisfaction']}")
                    st.write(f"**Transferir:** {response_info['transfer']}")
                    st.write(f"**Finalizar:** {response_info['finish']}")

                    # Mostrar citas si están disponibles
                    if response_info.get("citations"):
                        st.write("**Citas:**")
                        for i, citation in enumerate(response_info["citations"][:3]):  # Mostrar máximo 3 citas
                            option = citation.get("metadata", {}).get("option", "N/A")
                            st.write(f"- {option}")

            # Agregar respuesta del asistente al historial
            st.session_state.messages.append({
                "role": "assistant",
                "content": response_text,
                "timestamp": response_timestamp,
                "metadata": response_info
            })
