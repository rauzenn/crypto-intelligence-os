# 1. JARVIS REPOSITORY AUDIT REPORT

## Hangi modül gerçekten çalışıyor?
- **Data Ingestion (Coingecko & DexScreener):** Gerçekten çalışıyor. API'ye istek atıp veri alıyor.
- **Normalization:** Gerçekten çalışıyor. `NormalizedEvent` nesnesine dönüştürüyor.
- **Database Persistence:** Gerçekten çalışıyor. `events` tablosuna yazıyor.
- **Dashboard (Streamlit):** Gerçekten çalışıyor. DB'den okuyup gösteriyor.
- **Telegram Bot:** Gerçekten çalışıyor (API çalışırsa mesaj atıyor, komut dinliyor).
- **Background Worker (ARQ):** Gerçekten çalışıyor. Ingestion döngüsünü tetikliyor.

## Hangisi sadece skeleton / mock / prototype?
- **Wallet Hunter 2.0:** Prototiptir. `run_wallet_hunter_cycle` task'ı içinde sadece placeholder var, geçmiş DB işlemleriyle wallet cluster analizi yapmıyor.
- **Alpha Radar (Anomaly Detection):** Mock verilerle (Hack to simulate anomaly) çalışıyor. Gerçekte geçmiş veriyi veritabanından çekip hareketli ortalama hesaplamıyor.
- **Narrative Engine:** Keyword mapping yapıyor ancak sosyal ağlardan (Twitter/Telegram) akan sürekli bir mesaj akışı (stream) olmadığı için gerçek bir ölçüm yapamıyor. Sadece skeleton.
- **Chain Discovery:** Event history alıp hesaplama mantığı yazıldı ama DB'den periyodik chain metrikleri alıp bunu hesaplayan bir worker task'ı yok. Skeleton.
- **Risk Engine:** Sadece sabit contract kural setleri var, on-chain contract tarama (Alchemy/Helius üzerinden) fonksiyonları skeleton.
- **Outcome Engine (Learning):** Modeli ve fonksiyonu var ama zamanı gelince T+1h, T+6h snapshot alan ve geçmiş alertleri test eden background döngüsü (job) yazılmadı. Skeleton.
- **Reputation System:** Fonksiyonları var ama neye göre puan düşüreceğine karar veren mantık Outcome Engine'e bağlı olduğu için henüz çalışmıyor. Skeleton.

## Hangi adapter gerçek API'ye bağlı ve hangisi veri döndürüyor?
- **CoinGecko:** BAĞLI VE ÇALIŞIYOR.
- **DexScreener:** BAĞLI VE ÇALIŞIYOR.
- Diğerleri (Alchemy, Helius, News, Telegram Ingest): API key olmadığı için veya sadece skeleton oldukları için boş dönüyor.

## Hangi veri DB'ye yazılıyor / Intelligence pipeline'a giriyor?
- DexScreener ve CoinGecko'dan alınan piyasa ve fiyat verileri DB'ye yazılıyor.
- Intelligence pipeline'ına (Alpha Radar'a) aktarılıyor ancak Alpha Radar'ın içindeki `context` (sosyal bahsedilme, geçmiş hacim) sahte.

## Eksik Altyapılar:
- Migration sistemi (Alembic) yok. Schema değişirse tablolar drop edilmek zorunda.
- Test coverage sadece `test_run.py` ile sınırlı, "historical replay" ve unit testler yok.
- Event Bus / Stream layer (Kafka/RabbitMQ/Redis PubSub) zayıf, her şey doğrudan DB ve worker'ın belleği üzerinde.
- "Jarvis Memory" veya Knowledge Graph (Node/Edge yapısı) henüz kurulmadı.

**SONUÇ:** Sistem başarılı bir monolitik "data-fetcher and dumper" gibi çalışıyor. FAKE DATA yasaklandığı için Alert sistemi şu an "hiçbir şey bulamıyor" konumuna düşecek (ki olması gereken budur).
